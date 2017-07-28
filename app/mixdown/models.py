# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

import logging
import os
import uuid
import hashlib

from datetime import timedelta
from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from celery.task.control import revoke

from base.storage import OverwriteFileSystemStorage

from .remote import APIClient
from .tasks import render_playlist_task

log = logging.getLogger(__name__)


def get_mixdown_upload_path(instance, filename):
    path = [instance._meta.app_label.lower()]
    path += str(instance.uuid).split('-')
    path += [filename]
    return os.path.join(*path)


class Playlist(models.Model):
    STATUS_INIT = 0
    STATUS_PENDING = 1
    STATUS_PROCESSING = 2
    STATUS_DONE = 3
    STATUS_ERROR = 99

    STATUS_CHOICES = (
        (STATUS_INIT, 'Initialized'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_DONE, 'Done'),
        (STATUS_ERROR, 'Error'),
    )

    status = models.PositiveSmallIntegerField(
        _('Status'),
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        blank=False, null=False,
        db_index=True,
    )

    # holds celery queue task id
    task_id = models.CharField(
        max_length=64, null=True, blank=True, editable=True,
    )

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, db_index=True
    )

    created = models.DateTimeField(
        auto_now_add=True, editable=False, db_index=True
    )
    updated = models.DateTimeField(
        auto_now=True, editable=False, db_index=True
    )

    remote_uri = models.URLField(
        null=True, blank=False, unique=True, db_index=True
    )

    duration = models.DurationField(
        null=True, blank=True
    )

    mixdown_file = models.FileField(
        null=True, blank=True,
        storage=OverwriteFileSystemStorage(), upload_to=get_mixdown_upload_path
    )

    content_hash = models.CharField(
        null=True, blank=True, max_length=64
    )

    def __str__(self):
        return '{}'.format(self.uuid)


@receiver(pre_save, sender=Playlist)
def playlist_pre_save(sender, instance, **kwargs):

    if not instance.pk:

        log.debug('object creation. will try to get data from remote api')
        r = APIClient().get(url=instance.remote_uri, params={'all': 'yes'})
        data = r.json()

        instance.pk = data['id']
        instance.uuid = data['uuid']
        instance.duration = timedelta(milliseconds=data['duration'])

        instance.status = Playlist.STATUS_PENDING

    else:

        if hasattr(instance, '_skip_content_hash_check') and instance._skip_content_hash_check:
            return

        # check playlist content and reprocess if changed
        r = APIClient().get(url=instance.remote_uri, params={'all': 'yes'})
        data = r.json()

        content_hash = hashlib.sha1(str(data['items']).encode('utf-8')).hexdigest()

        if content_hash != instance.content_hash:
            instance.status = Playlist.STATUS_PENDING
            instance.content_hash = content_hash


@receiver(post_save, sender=Playlist)
def playlist_post_save(sender, instance, **kwargs):

    if instance.status < Playlist.STATUS_PROCESSING:

        log.debug('Playlist {} needs processing'.format(instance.pk))

        # check for running task - terminate if found
        if instance.task_id:
            log.info('task {} running - need to terminate.'.format(instance.task_id))
            revoke(instance.task_id, terminate=True, signal='SIGKILL')

        celery_task = render_playlist_task.apply_async((instance,))
        Playlist.objects.filter(pk=instance.pk).update(task_id=celery_task.id)

        # just for debuging - the non-async version
        # render_playlist_task(instance)


@receiver(post_delete, sender=Playlist)
def playlist_post_delete(sender, instance, **kwargs):

    if instance.mixdown_file:
        if os.path.isfile(instance.mixdown_file.path):
            os.remove(instance.mixdown_file.path)
