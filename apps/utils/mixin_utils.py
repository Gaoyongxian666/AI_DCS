# -*- coding: utf-8 -*-
__author__ = 'bobby'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    # 一个软件实体应当对扩展开放，对修改封闭。
    #
    # 开：是指对于组件功能的扩展是开放的，是允许对其进行功能扩展的。
    #
    # 闭：是指对于原有代码的修改是封闭的，即不修改原有的代码

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)