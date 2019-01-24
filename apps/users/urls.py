
# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2018/9/27'

"""
from django.conf.urls import url
from django.urls import path

from users.views import UserinfoView, UploadImageView, UpdatePwdView, MyFavWorksView, MyLoveWorksView, MyWorksView, \
    MyMessageView

urlpatterns = [
    #用户信息
    path('info/', UserinfoView.as_view(), name="user_info"),

    #用户头像上传
    path('image/upload/', UploadImageView.as_view(), name="image_upload"),

    #用户个人中心修改密码
    path('update/pwd/', UpdatePwdView.as_view(), name="update_pwd"),

    path('myfav/works/', MyFavWorksView.as_view(), name="myfav_works"),

    path('mylove/works/', MyLoveWorksView.as_view(), name="mylove_works"),

    path('my/works/', MyWorksView.as_view(), name="my_works"),

    path('message/', MyMessageView.as_view(), name="my_message"),

]