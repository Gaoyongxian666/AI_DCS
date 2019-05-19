# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2018/12/2'

"""
from __future__ import absolute_import, unicode_literals

from celery import Celery



app = Celery('AIDCS', broker='redis://127.0.0.1:6379/0',backend="redis://127.0.0.1:6379/0",include=['AIDCS.tasks'])

#do_sketch.delay("/home/ai/AI_DCS/AIDCS/input/gray.jpg","/home/ai/AI_DCS/AIDCS/gray.jpg")

