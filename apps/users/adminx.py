# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2018/9/19'

"""
import xadmin
from .models import UserProfile,Banner


class UserProfileAdmin(object):
    pass

class BannerAdmin(object):
    pass

xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(Banner,BannerAdmin)

from xadmin import views
class BaseSetting(object):
    # 开启主题功能
    enable_themes=True
    use_bootswatch=True
xadmin.site.register(views.BaseAdminView,BaseSetting)


# x admin 全局配置参数信息设置
class GlobalSettings(object):
    site_title = "AIDCS  后台管理"
    site_footer = "AIDCS"
    # 收起菜单
    # menu_style = "accordion"
# 将头部与脚部信息进行注册:
xadmin.site.register(views.CommAdminView, GlobalSettings)