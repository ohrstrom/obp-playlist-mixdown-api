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
        lookup_field='id'
    )

    remote_uri = serializers.URLField(
        validators=[
            RemoteURIAccepted(),
            RemoteURIReadable(),
            UniqueValidator(queryset=Playlist.objects.all())
        ]
    )

    remote_absolute_url = serializers.URLField(
        read_only=True
    )

    mixdown_file = serializers.FileField(
        read_only=True
    )

    status_display = serializers.SerializerMethodField()

    def get_status_display(self, obj):
        return '{}'.format(obj.get_status_display())

    eta = serializers.SerializerMethodField()

    def get_eta(self, obj):

        eta = 0

        if obj.status < obj.STATUS_DONE:

            eta =  (obj.updated + timedelta(seconds=obj.target_duration / 10)-timezone.now()).total_seconds()

        return eta

    class Meta:
        model = Playlist
        depth = 1
        fields = [
            'url',
            'remote_uri',
            'remote_absolute_url',
            'mixdown_file',
            'uuid',
            'status',
            'status_display',
            'eta',
        ]
