# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2018/10/6'

"""
import xadmin
from operation.models import WorksComments, UserFavorite, UserWorks,UserMessage


class WorksCommentsAdmin(object):
    pass
class UserFavoriteAdmin(object):
    pass
class UserWorksAdmin(object):
    pass
class UserMessageAdmin(object):
    pass

xadmin.site.register(UserWorks,UserWorksAdmin)
xadmin.site.register(WorksComments,WorksCommentsAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
