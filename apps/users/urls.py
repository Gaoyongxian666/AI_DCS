
# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2018/9/27'

"""
from django.conf.urls import url
from django.urls import path

from users import views
from users.views import UserinfoView, UploadImageView, UpdatePwdView, MyFavWorksView, MyLoveWorksView, MyWorksView, \
    MyMessageView, WXUserinfoView, WXUploadImageView, WXMyFavWorksView, WXMyWorksView, WXMyLoveWorksView

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
    # 微信api:
    path('test/', views.test_session),
    path('test2/', views.test_session2),

    path('authorize', views.authorize, name='authorize'),
    path('logout', views.wxlogout, name='logout'),
    path('wxinfo/', WXUserinfoView.as_view(), name="wxuser_wxinfo"),
    path('wximage/upload/', WXUploadImageView.as_view(), name="wximage_upload"),
    path('wxmyfav/works/', WXMyFavWorksView.as_view(), name="wxmyfav_works"),
    path('wxmylove/works/', WXMyLoveWorksView.as_view(), name="wxmylove_works"),
    path('wxmy/works/', WXMyWorksView.as_view(), name="wxmy_works"),

    path('status', views.get_status, name='get_status'),

]