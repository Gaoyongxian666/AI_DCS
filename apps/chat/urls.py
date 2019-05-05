# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2018/11/30'

"""
from django.conf.urls import url

from . import views

urlpatterns = [
    # 前面不要有/
    # url(r'^/chat/$', views.index),

    url(r'^chat/$', views.index),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),

]