# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2019/5/19'

"""

import redis
import json
class RedisQueue(object):
    def __init__(self, name, namespace='queue', **redis_kwargs):
       # redis的默认参数为：host='localhost', port=6379, db=0， 其中db为定义redis database的数量
       self.__db= redis.Redis(**redis_kwargs)
       self.key = '%s:%s' %(namespace, name)

    def qsize(self):
        return self.__db.llen(self.key)  # 返回队列里面list内元素的数量

    def put(self, item):
        self.__db.rpush(self.key, item)  # 添加新元素到队列最右方

    def get_wait(self, timeout=None):
        # 返回队列第一个元素，如果为空则等待至有元素被加入队列（超时时间阈值为timeout，如果为None则一直等待）
        item = self.__db.blpop(self.key, timeout=timeout)
        # if item:
        #     item = item[1]  # 返回值为一个tuple
        return item

    def get_nowait(self):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.__db.lpop(self.key)
        return item

    def clean(self):
        item = self.__db.delete(self.key)
        return item

    def get_all(self):
        wait_task = self.__db.lrange(self.key, 0, 1000)
        wait_task_list=[]
        for wait_task_ in wait_task:
            task_dict = json.loads(wait_task_.decode("utf8"))
            wait_task_list.append(task_dict)
        return  wait_task_list

    def finish_task(self,task_id):
        self.__db.rpush(task_id, "ok")
        self.__db.expire(task_id,300)
        return  True
