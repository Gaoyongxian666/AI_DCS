# # import pymysql
# # pymysql.install_as_MySQLdb()
# import json
#
# import redis
# from celery import Celery
# from celery.result import AsyncResult
#
#
# # for i in range(0,8):
# #     task=add.delay(1,1)
# #     print(task)
#
# # app.control.revoke(task_id="e6cb7989-cff7-4414-81a2-6d8b98f1603b")
#
# # concurrency: 1 (eventlet)
# # celery -A tasks worker -l info -P eventlet -c 1
#
# # result=AsyncResult(id="b70f4b81-542f-4e36-b558-33b3f82c111a",backend="redis://127.0.0.1:6379/0")
# # # result.successful()
# # print(result.result)
#
# app = Celery('AIDCS',
#              broker='redis://127.0.0.1:6379/0',
#              backend='redis://127.0.0.1:6379/0',
#              include=['AIDCS.tasks'])
# # print(app.result)
# # # app.control.revoke(task_id="d34d89a2-5bcb-46d3-bb42-8408532d722e")
# # print(app.AsyncResult)
#
# r = redis.Redis(host='127.0.0.1',port=6379)
# wait_task = r.lrange('celery', 0, 100)
# for wait_task_ in wait_task:
#     task_dict=json.loads(wait_task_.decode("utf8"))
#     print(task_dict["body"])
#     print(task_dict["headers"]["id"])
#
# # keys=r.keys(pattern="celery-task-meta-*")
#
# keys=r.keys(pattern="celery")
# # 必须从开头开始匹配
# # 通配符写空
# print(keys)
#
# len=r.llen("celery")
# print(len)
# for key in keys:
#     print(str(key.decode("utf8")))
#
# wait_task = r.lrange('celery', 0, 100)
# print(wait_task)
# # wait_task.reverse()
