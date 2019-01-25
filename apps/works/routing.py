# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2018/11/30'

"""


# chat/routing.py
from django.conf.urls import url
from django.urls import path

from . import consumers


# 不同用户的socket，把他们加入到不同的组中
# 因为一个url就代表着一个socket连接，不同的socket就需要不同的名称
# 如果他们都访问一个ws连接，说明他们都加入了同一个room
# 如果你想保持一个独立的socket连接，你就必须建立一个单独的连接
# 推荐使用类视图
websocket_urlpatterns = [
    path('ws/task/<str:task_id>/', consumers.MyConsumer),

    # url(r'^ws/task/(?P<active_code>.*)/$', consumers.MyConsumer),
]

