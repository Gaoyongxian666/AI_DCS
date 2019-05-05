from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import time
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from celery.app.control import Control
from tasks import app
import redis
import subprocess


class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.accept()

        r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=0)

        i=0
        while True:
            i = i + 1
            time.sleep(2)
            if i>80:
                i=80

            cur_task_id_name = 'celery-task-meta-'+self.task_id
            flag = r.exists(cur_task_id_name)

            if flag:
                r.delete(cur_task_id_name)
                i=100
                self.send(text_data=json.dumps({
                    "progress": i,
                    "message": "任务完成"
                }))
                print("任务完成，删除任务")
                break


            # 正在执行
            (status, output) = subprocess.getstatusoutput('celery -A tasks inspect active')
            print(output)
            output_list = output.split("*")
            print(output_list)
    
            if len(output_list)>=2:
                active_list = []
                for output_str in output_list[1:]:
                    print(output_str)
                    active_task_one_str=output_str.replace("'", "\"").replace("None", '"None"').replace("False", '"False"').replace("True", '"True"')
                    print(active_task_one_str)
                    active_task_one_dict = json.loads(active_task_one_str)
                    active_task_id_=active_task_one_dict["id"]
                    active_list.append(active_task_id_)
                if self.task_id in active_list:
                    i=50
                    self.send(text_data=json.dumps({
                        "progress": i,
                        "message": "您的作品正在生成...."
                    }))



            # 第一个等待工程
            (status, output) = subprocess.getstatusoutput('celery -A tasks inspect reserved')
            output_list = output.split("*")
            if len(output_list) >= 2:
                first_wait_task_one_str = output_list[1].replace("'", "\"").replace("None", '"None"').replace("False",'"False"').replace("True", '"True"')
                first_wait_task_one_dict = json.loads(first_wait_task_one_str)
                first_wait_task_id_ = first_wait_task_one_dict["id"]
                if self.task_id == first_wait_task_id_:
                    self.send(text_data=json.dumps({
                        "progress": i,
                        "message": "请稍等，您前面还有1人"
                    }))


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
                    number=index+1
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
        self.close()
        myControl = Control(app)
        myControl.revoke(task_id=self.task_id, terminate=True)
        print("不正常去除任务")



    # accept（）不执行完，就不会执行receive
    def receive(self, text_data):
        pass







