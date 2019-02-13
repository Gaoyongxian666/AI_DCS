from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import time
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from celery.app.control import Control
from AIDCS.celery import app
import redis
import subprocess


class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.accept()

        r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=0)

        i = 0
        while True:
            i = i + 1
            time.sleep(2)
            if i > 80:
                i = 80
            self.send(text_data=json.dumps({
                "progress": i,
                "message": "正在生成中。。。。"
            }))

            cur_task_id_name = 'celery-task-meta-' + self.task_id
            flag = r.exists(cur_task_id_name)

            if flag:
                r.delete(cur_task_id_name)
                i = 100
                self.send(text_data=json.dumps({
                    "progress": i,
                    "message": "任务完成"
                }))
                print("任务完成，删除任务")
                break

            # 取前一百个等待队列
            wait_task = r.lrange('celery', 0, 100)
            wait_task.reverse()

            print(wait_task)
            index = 0
            for wait_task_one in wait_task:
                index = index + 1
                print(wait_task_one)
                wait_task_one_dict = json.loads(wait_task_one)
                task_id_ = wait_task_one_dict["headers"]["id"]
                if self.task_id == task_id_:
                    # 记得加一个
                    number = index + 1
                    self.send(text_data=json.dumps({
                        "progress": i,
                        "message": "请稍等，您前面还有%d人" % number
                    }))
                    print(index)
                    break




                    # if i>=6:
                    #     print('kaishi   ')
                    #     myControl=Control(app)
                    #     myControl.revoke(task_id=self.task_id, terminate=True)
                    #     print("jieshu")
                    #     break

    def disconnect(self, close_code):
        print("dis")
        print("disdssssssssssssssssss")

        self.close()
        app.control.revoke(task_id=self.task_id)
        print("不正常去除任务")

    # accept（）不执行完，就不会执行receive
    def receive(self, text_data):
        pass







