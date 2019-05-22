import redis
from asgiref.sync import async_to_sync
from celery import Celery
from channels.generic.websocket import WebsocketConsumer
import time
from channels.generic.websocket import AsyncWebsocketConsumer
import json


# 这是一个同步WebSocket使用者，它接受所有连接，从其客户端接收消息，并将这些消息回送到同一客户端。
# 1 对 1
# 同步的可以使用 while True
# class ChatConsumer1(WebsocketConsumer):
#     def connect(self):
#         print("begin")
#         self.accept()
#
#     def disconnect(self, close_code):
#         print("dis")
#         self.close()
#         pass
#
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         print(message)
#         while True:
#             time.sleep(2)
#             print("后台收到"+message)
#             self.send(text_data=json.dumps({
#             'message': message
#         }))
#
#
#
#
#
# # 当用户发布消息时，JavaScript函数将通过WebSocket将消息传输到ChatConsumer。
# # ChatConsumer将接收该消息并将其转发到与房间名称对应的组。
# # 然后，同一组中的每个ChatConsumer（因此在同一个房间中）将接收来自该组的消息，并通过WebSocket将其转发回JavaScript，并将其附加到聊天日志中。
# # 1 对 N
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         # 字典的读取方法
#         # 从chat / routing.py中的URL路由获取 'room_name' 参数，该参数打开与使用者的WebSocket连接。
#         # 每个使用者都有一个范围(scope)，其中包含有关其连接的信息，特别是包括URL路由中的任何位置或关键字参数以及当前经过身份验证的用户（如果有）。
#
#         self.room_group_name = 'wwwwwwwwwwwww'
#         # 直接从用户指定的房间名称构造Channels组名称，不进行任何引用或转义。
#         # 组名只能包含字母，数字，连字符和句点。因此，此示例代码将在具有其他字符的房间名称上失败。
#
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         print("当前频道名称"+self.channel_name)
#         print("当前频道别名"+self.room_name)
#         print("当前通道层名称"+self.room_group_name)
#
#
#
#         # 加入一个团队。
#         # async_to_sync（...）包装器是必需的，因为ChatConsumer是同步WebsocketConsumer，但它调用异步通道层方法。
#         # （所有通道层方法都是异步的。）组名仅限于ASCII字母数字，连字符和句点。
#         # 由于此代码直接从房间名称构造组名称，因此如果房间名称包含在组名称中无效的任何字符，则该名称将失败。
#
#
#         self.accept()
#         # 接受WebSocket连接。
#         # 如果不在connect（）方法中调用accept（），则拒绝并关闭连接。
#         # 例如，您可能希望拒绝连接，因为请求的用户无权执行请求的操作。如果您选择接受连接，建议将accept（）作为connect（）中的最后一个操作。
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 "type": "chat_message",
#                 'message': None,
#                 "text": self.room_name+"已经加入聊天频道",
#             },
#         )
#         print(self.room_name+'向通道层'+self.room_group_name+"发送消息："+self.room_name+"已经加入聊天频道")
#
#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 "type": "chat_message",
#                 'message': None,
#                 "text": self.room_name + "已经退出聊天频道",
#             },
#         )
#         print(self.room_name+'向通道层'+self.room_group_name+"发送消息："+self.room_name+"已经退出聊天频道")
#
#
#     # Receive message from WebSocket
#     # 接收客户端发回的消息
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         print('获取前端传回消息'+message)
#
#         self.send(text_data=json.dumps({
#             'message': '各自频道发回前端的消息'
#         }))
#
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'text':None
#             }
#         )
#         print(self.room_name+'向通道层'+self.room_group_name+"发送消息："+message)
#         # 将事件发送给房间组。
#         # 事件具有特殊的“类型”键，该键对应于应该在接收事件的使用者上调用的方法的名称。
#
#
#
#     # Receive message from room group
#     # 给每个客户端发送消息,聊天室后台发送消息，channel后台获取回调
#     # 可以给自己单独发送消息
#     def chat_message(self, event):
#         print('Receive message from room group')
#         if event['message']:
#             self.send(text_data=json.dumps({
#                 'message': '接收频道发回的消息：'+event['message']
#             }))
#
#
#         if event['text']:
#             # Send message to WebSocket
#             self.send(text_data=json.dumps({
#                 'message': '通道层有人加入或者退出：'+event['text']
#             }))




# 异步实现
# 没有办法实现while True
class ChatConsumer2(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.room_group_name = 'aidcs_task'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': "chat_message",
                'message': self.task_id+":已经加入聊天频道",
                'chat_type': 0  # 标式每个人都要检测自己的状态
            }
        )

    async def disconnect(self, close_code):
        print(self.task_id+":websocket已经断开")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': "chat_message",
                'message': self.task_id + "已经离开聊天频道",
                'chat_type': 0 # 标式每个人都要检测自己的状态
            }
        )
        await self.close()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )




    # Receive message from WebSocket 名字对应 type
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("收到前端发送的消息："+message)



    # 接收到服务器后台消息
    async def chat_message(self, event):
        print("接收到服务器后台消息")
        print(event['message'])
        type=event['chat_type']
        print(type)
        if type==0:
            info=get_info(self.task_id)
            if info=="already":
                print("already")
                pass
            else:
                print("ok")
                task_status=is_ok(self.task_id)
                my_sum=info["sum"]
                position=info["position"]
                await self.send(text_data=json.dumps({
                    "message": "正常",# 触发轮询
                    'position': position,
                    'sum':my_sum,
                    'task_status':task_status
                }))
        if type==1:
            await self.send(text_data=json.dumps({
                'message': event['message']
            }))



def get_info(task_id):
    r = redis.Redis(host='127.0.0.1', port=6379,db=1)
    wait_task = r.lrange('queue:aidcs', 0, 1000)
    sum=len(wait_task)+1
    n=1
    print(wait_task)
    # 不能判断wait——task为空
    if sum==1:
        print("队列为空")
        return {"position":1,"sum":sum}
    else:
        for wait_task_ in wait_task:
            try:
                n=n+1
                task_dict = json.loads(wait_task_.decode("utf8"))
                resis_task_id=task_dict["task_id"]
                if task_id==resis_task_id:
                    return {"position":n,"sum":sum}
            except:
                print("task_id解析错误")
                return "already"
        return "already"


def is_ok(task_id):
    r = redis.Redis(host='127.0.0.1', port=6379,db=1)
    cur_task_id_name =task_id
    flag = r.exists(cur_task_id_name)
    if flag:
        r.delete(cur_task_id_name)
        print("执行完成，删除key")
        return True
    else:
        print("不存在key")
        return False


