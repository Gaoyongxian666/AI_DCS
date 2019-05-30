# # from websocket import create_connection
# #
# # def do_ws():
# #     try:
# #         ws = create_connection("ws://106.13.37.131/ws/chat/task_queue/")
# #         print("Sending 'Hello, World'...")
# #         ws.close()
# #     except:
# #         print("websocket错误")
# #
# # do_ws()
#
# import threading
# import time
#
# def run():
#     time.sleep(2)
#     print('当前线程的名字是： ', threading.current_thread().name)
#     time.sleep(2)
#
#
# if __name__ == '__main__':
#
#     start_time = time.time()
#
#     print('这是主线程：', threading.current_thread().name)
#
#     t = threading.Thread(target=run)
#     t.start()
#     t.join(1)
#
#     # thread_list = []
#     # for i in range(5):
#     #     t = threading.Thread(target=run)
#     #     thread_list.append(t)
#     #
#     # for t in thread_list:
#     #     t.setDaemon(True)
#     #     t.start()
#     #
#     # for t in thread_list:
#     #     t.join(timeout=1)
#
#     print('主线程结束了！' , threading.current_thread().name)
#     print('一共用时：', time.time()-start_time)