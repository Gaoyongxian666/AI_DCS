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
'''


upstream yixiang {
    server unix:///virtualenvs/shenmo/yixiang/yx.sock;
}
server {
    listen 80;
    server_name _;
    return 444; # 过滤其他域名的请求，返回444状态码
}
# 配置服务器
server {
    # 监听的端口号
    listen      80;
    # 域名
    server_name   39.106.1.99;
    charset     utf-8;

    # 最大的文件上传尺寸
    client_max_body_size 75M;

    # 静态文件访问的url
    location /static {
        # 静态文件地址
        alias /virtualenvs/shenmo/yixiang/front/dist;
    }

    # 最后，发送所有非静态文件请求到django服务器
    location / {
        uwsgi_pass yixiang;
        # uwsgi_params文件地址
        include     /etc/nginx/uwsgi_params;
    }
}

server {
     listen 80;
     server_name shenmos.com;
            location ^~/ {
                proxy_set_header Accept-Encoding "";
                proxy_set_header Referer "http://106.13.37.131/";
                proxy_pass http://106.13.37.131/;
                add_header Access-Control-Allow-Origin *;
                sub_filter 'http://106.13.37.131' 'http://shenmos.com';
                sub_filter_types text/css text/xml text/html text/javascript application/json application/javascript;
                sub_filter_once off;
                }
             location ~* \.(?:css|js|ttf|woff|svg|ico|png|jpg)$ {
                        proxy_set_header Accept-Encoding "";
                        proxy_set_header Referer "http://106.13.37.131/";
                        proxy_pass http://106.13.37.131/$request_uri;

                        add_header Access-Control-Allow-Origin *;

                        sub_filter 'http://106.13.37.131' 'http://shenmos.com';
                        sub_filter_types text/css text/xml text/html text/javascript application/javascript application/json;
                        sub_filter_once off;
                    }
}
server {
         listen 443 http2;
         server_name shenmos.com;
         ssl on;
         ssl_certificate   /etc/nginx/1271276_shenmos.com.pem;
         ssl_certificate_key  /etc/nginx/1271276_shenmos.com.key;
         ssl_session_timeout 5m;
         ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
         proxy_redirect  http:// https://;
         ssl_ciphers  HIGH:!aNULL:!MD5;
         ssl_prefer_server_ciphers on;
                    location ^~/ {
                        proxy_pass http://106.13.37.131:80;
                        proxy_set_header Accept-Encoding "";
                        proxy_set_header Referer "http://106.13.37.131/";
                        add_header Access-Control-Allow-Origin *;
                        sub_filter 'http://106.13.37.131' 'https://shenmos.com';
                        sub_filter_types text/css text/xml text/html text/javascript application/json application/javascript;
                        sub_filter_once off;
                    }
                    location ~* \.(?:css|js|ttf|woff|svg|ico|png|jpg)$ {
                        proxy_set_header Accept-Encoding "";
                        proxy_set_header Referer "http://106.13.37.131/";
                        proxy_pass http://106.13.37.131/$request_uri;

                        add_header Access-Control-Allow-Origin *;

                        sub_filter 'http://106.13.37.131' 'https://shenmos.com';
                        sub_filter_types text/css text/xml text/html text/javascript application/javascript application/json;
                        sub_filter_once off;
                    }
}

                        proxy_set_header X-Real-Ip $remote_addr;
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        proxy_set_header X-Forwarded-Proto https;
                                                proxy_set_header Host $host;




'''