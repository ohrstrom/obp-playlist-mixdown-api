# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta
from django.utils import timezone

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..models import Playlist
from ..remote import APIClient, API_BASE_URL


class RemoteURIAccepted(object):
    def __call__(self, value):
        if not value.startswith(API_BASE_URL):
            message = 'Invalid URI. Must start with: {}'.format(API_BASE_URL)
            raise serializers.ValidationError(message)


class RemoteURIReadable(object):
    def __call__(self, value):

        c = APIClient()

        try:
            r = c.get(url=value, params={'all': 'yes'})
        except Exception as e:
            message = 'Remote API error: {}'.format(e)
            raise serializers.ValidationError(message)

        if not r.status_code == 200:
            message = 'Remote API error: {}'.format(r.status_code)
            raise serializers.ValidationError(message)


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:playlist-detail',
        lookup_field='uuid'
    )

    uuid = serializers.UUIDField()

    remote_uri = serializers.URLField(
        validators=[
            RemoteURIAccepted(),
            RemoteURIReadable(),
            UniqueValidator(queryset=Playlist.objects.all())
        ]
    )

    mixdown_file = serializers.FileField(
        read_only=True
    )

    duration = serializers.DurationField(
        read_only=True
    )

    content_hash = serializers.CharField(
        read_only=True
    )

    status_display = serializers.SerializerMethodField()

    def get_status_display(self, obj):
        return '{}'.format(obj.get_status_display()).lower()

    eta = serializers.SerializerMethodField()

    def get_eta(self, obj):

        eta = obj.updated

        if obj.status < obj.STATUS_DONE:

            #eta = (obj.updated + (obj.duration / 10) - timezone.now()).total_seconds()
            eta = obj.updated + (obj.duration / 10)

        return eta

    class Meta:
        model = Playlist
        depth = 1
        fields = [
            'url',
            'remote_uri',
            'mixdown_file',
            'duration',
            'uuid',
            'status',
            'status_display',
            'content_hash',
            'eta',
        ]
