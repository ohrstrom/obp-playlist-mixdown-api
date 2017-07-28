# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import PlaylistSerializer
from ..models import Playlist


class PlaylistViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    queryset = Playlist.objects.all().order_by('-created')
    serializer_class = PlaylistSerializer
    lookup_field = 'uuid'

    def list(self, request, *args, **kwargs):

        queryset = Playlist.objects.filter().order_by('-created')

        serializer = PlaylistSerializer(
            queryset,
            many=True,
            context={'request': request}
        )

        return Response({
            'num_processing': queryset.filter(status=Playlist.STATUS_PROCESSING).count(),
            'results': serializer.data
        })

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()



    def get_or_create_detail(self, request, *args, **kwargs):

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            print(e)

        data = request.data
        data.update({
            'uuid': kwargs.get('uuid')
        })

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     instance.status = Playlist.STATUS_PENDING
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     return Response(serializer.data)



playlist_list = PlaylistViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
playlist_detail = PlaylistViewSet.as_view({
    'get': 'retrieve',
    'put': 'get_or_create_detail',
    'patch': 'update',
    'delete': 'destroy',
})
