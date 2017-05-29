# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.urlpatterns import format_suffix_patterns


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'mixdown': reverse('api:playlist-list', request=request, format=format),
    })



urlpatterns = [
    url(r'^$', api_root),
    url('^mixdown/', include('mixdown.api.urls')),
]
