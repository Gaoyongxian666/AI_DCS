# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2019/4/25'

"""

from django.conf.urls import url, include
from django.urls import path

from works.views import *

urlpatterns = [
    path('auth/', include('users.urls')),
    path('works/', include('works.urls'))

]