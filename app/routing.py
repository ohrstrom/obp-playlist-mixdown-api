# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from notification import consumers
from notification.routing import notification_routing
from channels import route
from channels.routing import include


channel_routing = [
    # You can use a string import path as the first argument as well.
    include(notification_routing, path=r"^/notification/stream"),
]
