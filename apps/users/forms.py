# -*- coding: utf-8 -*-

"""

__title__ = ''

__author__ = 'g1695'

__mtime__ = '2018/9/19'

"""


from django import forms
from captcha.fields import CaptchaField

from users.models import UserProfile


# 注意 前面的变量名就是 在模板里标签的变量名
# 通过这个可以检查form产过来的东西是否正确

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # 在前端向后台发送信息的时候会验证，如果错了，可以直接由字段直接打印
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ModifyPwdForm(forms.Form):
    password0 = forms.CharField(required=True, min_length=5)
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'signature', 'address', 'mobile']



class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
