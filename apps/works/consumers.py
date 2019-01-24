from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import time
from channels.generic.websocket import AsyncWebsocketConsumer
import json


# 这是一个同步WebSocket使用者，它接受所有连接，从其客户端接收消息，并将这些消息回送到同一客户端。
# 1 对 1
# 同步的可以使用 while True
class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("begin")




    def disconnect(self, close_code):
        print("dis")
        self.close()
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data)
        message = text_data_json['message']
        print(message)
        i=0
        while True:
            i=i+1
            time.sleep(2)
            print("后台收到"+message)
            self.send(text_data=json.dumps({
            'message': i
        }))




