# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2018/10/6'

"""

from django.conf.urls import url, include
from django.urls import path

from works.views import *

urlpatterns = [
    #课程列表页
    path('list/', WorksListView.as_view(), name="works_list"),

    #课程详情页
    # \d 表示匹配的是数字 + 表示重复一次或者多次
    path('detail/<int:work_id>/', WorksDetailView.as_view(), name="works_detail"),

    path('download/<int:work_id>/', DownloadView.as_view(), name="download"),

    path('add_fav/', AddFavView.as_view(), name="add_fav"),

    path('add_love/', AddLoveView.as_view(), name="add_love"),

    path('add_download/', DownloadView.as_view(), name="add_download"),

    path('add_comment/', AddComentsView.as_view(), name="add_comment"),

    path('GenerateGrayView/', GenerateGrayView.as_view(), name="generategray"),

    path('GenerateLineArtView/', GenerateLineArtView.as_view(), name="generatelineart"),

    path('GenerateLineView/', GenerateLineView.as_view(), name="generateline"),

    path('GenerateFigureView/', GenerateFigureView.as_view(), name="generatefigure"),

    path('GenerateLogoView/', GenerateLogoView.as_view(), name="generatelogo"),

    path('GenerateStyleView/', GenerateStyleView.as_view(), name="generatestyle"),

    path('GenerateChineseView/', GenerateChineseView.as_view(), name="generatechinese"),

    # url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    #
    # #课程评论
    # url(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name="course_comments"),
    #
    # #添加课程评论
    # url(r'^add_comment/$', AddComentsView.as_view(), name="add_comment"),

# 微信api：
#课程列表页
    path('wxlist/', WXWorksListView.as_view(), name="wxworks_list"),
    path('wxdetail/<int:work_id>/', WXWorksDetailView.as_view(), name="wxworks_detail"),
    path('wxdownload/<int:work_id>/', DownloadView.as_view(), name="wxdownload"),
    path('wxadd_fav/', WXAddFavView.as_view(), name="wxadd_fav"),
    path('wxadd_love/', WXAddLoveView.as_view(), name="wxadd_love"),
    path('wxadd_download/', WXDownloadView.as_view(), name="wxadd_download"),

    # path('wxadd_comment/', AddComentsView.as_view(), name="add_comment"),

    path('wxGenerateGrayView/', GenerateGrayView.as_view(), name="generategray"),
    path('wxGenerateLineArtView/', GenerateLineArtView.as_view(), name="generatelineart"),
    path('wxGenerateLineView/', GenerateLineView.as_view(), name="generateline"),
    path('wxGenerateFigureView/', GenerateFigureView.as_view(), name="generatefigure"),
    path('wxGenerateLogoView/', GenerateLogoView.as_view(), name="generatelogo"),

    path('wxGenerateStyleView/', GenerateStyleView.as_view(), name="generatestyle"),

    path('wxGenerateChineseView/', GenerateChineseView.as_view(), name="generatechinese"),

]