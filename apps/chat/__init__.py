# # -*- coding: utf-8 -*-
#
# """
#
# __title__ = ''
#
# __author__ = 'g1695'
#
# __mtime__ = '2018/12/2'
#
# """
#
# # import os
# # import time
# # from datetime import timedelta
# # import sys
# #
# #
# # from __future__ import absolute_import, unicode_literals
# # from celery import Celery
# #
# #
# # app = Celery('AIDCS', broker='redis://127.0.0.1:6379/0',backend="redis://127.0.0.1:6379/0",include=['AIDCS.tasks'])
# #
# # @app.task
# # def add(content,output):
# #     pass
# #
# # #do_sketch.delay("/home/ai/AI_DCS/AIDCS/input/gray.jpg","/home/ai/AI_DCS/AIDCS/gray.jpg")
# #
# #
# # #do_ink.delay("/home/ai/AI_DCS/AIDCS/input/gray.jpg","/home/ai/AI_DCS/AIDCS/gray.jpg")
# # add.delay(4,4)
# import json
# import redis
# from celery import Celery
#
#
#
#
# taskid='a54ad6e2-3ff9-44d8-bacf-b8e5b8cf82b8'
#
#
# def get_info(task_id):
#     r = redis.Redis(host='127.0.0.1', port=6379)
#     wait_task = r.lrange('celery', 0, 100)
#     sum=len(wait_task)+2
#     reversed(wait_task)
#     n=3
#     for wait_task_ in wait_task:
#         task_dict = json.loads(wait_task_.decode("utf8"))
#         resis_task_id=task_dict["headers"]["id"]
#         if task_id==resis_task_id:
#             return {"position":n,"sum":sum}
#         n=n+1
#
#     else:return {"position":0,"sum":sum}
#
# d=get_info(taskid)
# print(d)
#
# def is_ok(task_id):
#     r = redis.Redis(host='127.0.0.1', port=6379)
#     cur_task_id_name = 'celery-task-meta-' + task_id
#     flag = r.exists(cur_task_id_name)
#     if flag:
#         r.delete(cur_task_id_name)
#         return True
#     else:
#         return False
#
# isok=is_ok(taskid)
# print(isok)
#
# app = Celery('AIDCS',
#              broker='redis://127.0.0.1:6379/0',
#              backend='redis://127.0.0.1:6379/0',
#              include=['AIDCS.tasks'])
# # print(app.result)
# app.control.revoke(task_id=taskid)
# # app.control.re