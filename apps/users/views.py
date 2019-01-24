import json

from django.core.paginator import PageNotAnInteger, Paginator
from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.urls import reverse
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from operation.models import UserFavorite, UserLove, UserWorks, UserMessage
from works.models import Works
from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ModifyPwdForm, UserInfoForm, UploadImageForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


# 可以让用户名和邮箱同时登陆
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 点击激活用户链接之后的逻辑
class AciveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")

# 点击注册按钮
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form":register_form, "msg":"用户已经存在"})
            pass_word = request.POST.get("password", "")
            send_register_email(user_name, "register")

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)

            user_profile.save()
	

            return HttpResponseRedirect(reverse("login"))

            #return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form":register_form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))

class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # is_valid方法，验证表单
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # 重定向到index的url
                    # 下面两种方式都是可以的
                    # return HttpResponseRedirect(reverse("index"))
                    # return HttpResponseRedirect('')这种方式返回的是login/
                    return  HttpResponseRedirect("/")

                else:
                    return render(request, "login.html", {"msg":"用户未激活！"})
            else:
                return render(request, "login.html", {"msg":"用户未激活或密码错误！"})
        else:
            return render(request, "login.html", {"login_form":login_form })

class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, "update_email")
        return HttpResponse('{"status":"success"}', content_type='application/json')

# class IndexView(View):
#     #慕学在线网 首页
#     def get(self, request):
#         #取出轮播图
#         all_banners = Banner.objects.all().order_by('index')
#         # courses = Course.objects.filter(is_banner=False)[:6]
#         # banner_courses = Course.objects.filter(is_banner=True)[:3]
#         # course_orgs = CourseOrg.objects.all()[:15]
#         return render(request, 'index.html', {
#             'all_banners':all_banners,
#             # 'courses':courses,
#             # 'banner_courses':banner_courses,
#             # 'course_orgs':course_orgs
#         })




# 通过modle创建的form表单验证，数据可以直接保存
class UserinfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'myCenter.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            print(json.dumps(user_info_form.errors))
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            # return JsonResponse('{"status":"success"}',safe=False)
            # return HttpResponseRedirect(reverse("users:user_info"))
            return HttpResponse(b'{"status":"success"}', content_type='application/json')
        else:
            # return JsonResponse('{"status":"fail"}',safe=False)
            return HttpResponse(b'{"status":"fail"}', content_type='application/json')







class MyFavWorksView(LoginRequiredMixin, View):

    def get(self, request):
        work_list = []
        fav_works = UserFavorite.objects.filter(user=request.user, fav_type=1).order_by("-add_time")
        for fav_work in fav_works:
            work_id = fav_work.fav_id
            try:
                work = Works.objects.get(id=work_id)
                work_list.append(work)

            except Exception:
                print(work_id)
                continue

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(work_list, 8)

        works = p.page(page)

        return render(request, 'myCollection.html', {
            # "work_list":work_list,
            # 不知道为什么work_list传入前端会没哟反应
            "work_list": works,
            "page": page,
            "p": p
        })

class MyLoveWorksView(LoginRequiredMixin, View):

    def get(self, request):
        work_list = []
        love_works = UserLove.objects.filter(user=request.user, love_type=1).order_by("-add_time")
        for love_work in love_works:
            work_id = love_work.love_id
            try:
                work = Works.objects.get(id=work_id)
                work_list.append(work)

            except Exception:
                print(work_id)
                continue


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(work_list, 8)

        works = p.page(page)

        return render(request, 'myLove.html', {
            # "work_list":work_list,
            # 不知道为什么work_list传入前端会没哟反应
            "work_list": works,
            "page": page,
            "p": p
        })

class MyWorksView(LoginRequiredMixin, View):

    def get(self, request):
        userworks_list = UserWorks.objects.filter(user=request.user).order_by("-add_time")
        works_list=[]

        for userworks in userworks_list:
            if userworks.works is not None:
                works_list.append(userworks.works)
            else:
                print(userworks.id)


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(works_list, 8)

        # work 这种外键不能在前端查询，要在后台查询

        works = p.page(page)



        return render(request, 'myWorks.html', {
            # "work_list":work_list,
            # 不知道为什么work_list传入前端会没哟反应
            "work_list": works,
            "page": page,
            "p": p
        })









# 我的消息
class MyMessageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        qunfa_message= UserMessage.objects.filter(user= 0)
        all_message = UserMessage.objects.filter(user= request.user.id)
        all_message=all_message|qunfa_message

        # 用户进入个人中心消息页面，清空未读消息记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个
        p = Paginator(all_message, 4)
        messages = p.page(page)
        return  render(request, "myMessage.html", {

            "messages":messages,
            "p":p,
            "page":page
        })

class UpdatePwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd0=request.POST.get("password0",'')
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            print(pwd0+'\n'+pwd2)
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            if authenticate(username=user.username, password=pwd0):
                user.password = make_password(pwd2)
                user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"原始密码错误"}', content_type='application/json')

        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class IndexView(View):
    # 当你报的错误在网上没有别人遇到，那八成是你懂了源码之类的东西，重装吧。
    def get(self, request):
        # 取出轮播图
        all_banner = Banner.objects.all().order_by('index')[1:3]
        first_banner = Banner.objects.all().order_by('index')[:1]

        # 灰度图上色
        chinese=Works.objects.all().filter(tag__icontains="水墨画生成").order_by('-love_nums')[:4]
        style=Works.objects.all().filter(tag__icontains="风格生成").order_by('-love_nums')[:4]
        logo=Works.objects.all().filter(tag__icontains="logo生成").order_by('-love_nums')[:4]
        lineart=Works.objects.all().filter(tag__icontains="线稿上色").order_by('-love_nums')[:4]
        figure=Works.objects.all().filter(tag__icontains="生成动漫").order_by('-love_nums')[:4]
        gray=Works.objects.all().filter(tag__icontains="灰度图上色").order_by('-love_nums')[:4]
        linege=Works.objects.all().filter(tag__icontains="生成线稿").order_by('-love_nums')[:4]


        # print(style)


        # 宽高比 1400-1900 ： 300-500   3:1

        # # 正常位课程
        # courses = Course.objects.filter(is_banner=False)[:6]
        # # 轮播图课程取三个
        # banner_courses = Course.objects.filter(is_banner=True)[:3]
        # # 课程机构
        # course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            "all_banner": all_banner,
            "first_banner": first_banner,
            "style":style,
            "logo": logo,
            "lineart": lineart,
            "figure": figure,
            "gray": gray,
            "chinese": chinese,
            "linege":linege


        })



def page_not_found(request):
    #全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    #全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response


