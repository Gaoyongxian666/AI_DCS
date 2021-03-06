"""AI_DCS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from operation import views
import xadmin
from users.views import LoginView, RegisterView, AciveUserView, LogoutView, IndexView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),

    path('', IndexView.as_view(), name="index"),
    path('index/', IndexView.as_view()),

    path('GenerateGray/', TemplateView.as_view(template_name='functionGray.html'), name="GenerateGray"),

    path('GenerateChinese/', TemplateView.as_view(template_name='functionChinese.html'), name="GenerateChinese"),

    path('GenerateLogo/', TemplateView.as_view(template_name='functionLogo.html'), name="GenerateLogo"),

    path('GenerateComic/', TemplateView.as_view(template_name='functionComic.html'), name="GenerateComic"),

    path('GenerateLineArt/', TemplateView.as_view(template_name='functionLineArt.html'), name="GenerateLineArt"),

    path('GenerateStyle/', TemplateView.as_view(template_name='functionStyle.html'), name="GenerateStyle"),

    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('captcha/', include('captcha.urls')),


    path('users/', include(('users.urls','users'), namespace="users")),

    path('works/', include(('works.urls','works'), namespace="works")),
    # include ( , 目录)
    path('api/v1.0/', include(('AI_DCS.version_1_0', 'AI_DCS'), namespace="api")),


    path('process_html/', views.process_html, name='process_html'),  # 处理数据的url, 当前页面的地址
    path('progressurl/', views.show_progress, name='progress'),  # 查询进度的url, 不需要html页面



    url(r'^active/(?P<active_code>.*)/$', AciveUserView.as_view(), name="user_active"),
    path('logout/', LogoutView.as_view(), name="logout"),

                  path('chat/', include('chat.urls')),




              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
