# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2018/10/6'

"""
import xadmin
from works.models import Works


class WorksAdmin(object):
    pass


xadmin.site.register(Works,WorksAdmin)
