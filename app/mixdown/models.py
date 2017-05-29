# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import uuid

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from .remote import APIClient
from .tasks import render_playlist_task

log = logging.getLogger(__name__)

RUN_ASYNC = True


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
        (STATUS_INIT, _('Initialized')),
        (STATUS_PENDING, _('Pending')),
        (STATUS_PROCESSING, _('Processing')),
        (STATUS_DONE, _('Done')),
        (STATUS_ERROR, _('Error')),
    )

    status = models.PositiveSmallIntegerField(
        _('Status'),
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        blank=False, null=False,
        db_index=True,
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

    remote_absolute_url = models.URLField(
        null=True, blank=False
    )

    target_duration = models.PositiveIntegerField(
        null=True, blank=True
    )

    mixdown_file = models.FileField(
        null=True, blank=True,
        upload_to=get_mixdown_upload_path
    )


@receiver(pre_save, sender=Playlist)
def playlist_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        log.debug('Object creation. Will try to get id from remote api')
        r = APIClient().get(url=instance.remote_uri, params={'all': 'yes'})
        data = r.json()
        instance.pk = data['id']
        instance.uuid = data['uuid']
        instance.target_duration = data['target_duration']
        instance.remote_absolute_url = '{}{}'.format('https://www.openbroadcast.org', data['absolute_url'])
        instance.status = Playlist.STATUS_PENDING


@receiver(post_save, sender=Playlist)
def playlist_post_save(sender, instance, **kwargs):
    if instance.status < Playlist.STATUS_PROCESSING:
        log.debug('Playlist {} needs processing'.format(instance.pk))

        if RUN_ASYNC:
            print('async')
            render_playlist_task.apply_async((instance,))
        else:
            print('sync')
            render_playlist_task(instance)
