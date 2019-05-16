import json
import os
import requests
from django.core.paginator import PageNotAnInteger, Paginator
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Root_DIR=os.path.dirname(os.path.dirname(BASE_DIR))


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
            return render(request, "login.html", {"login_form":login_form ,"message":"用户名密码格式错误"})

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




# 微信接口

from utils.response import wrap_json_response, ReturnCode, CommonResponseMixin
from utils.auth import c2s,already_authorized
def test_session(request):
    request.session['message'] = 'Test Django Session OK!'
    response = wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)

def test_session2(request):
    print('session content: ', request.session.items())
    response = wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)


def __authorize_by_code(request):
    '''
    使用wx.login的到的临时code到微信提供的code2session接口授权
    '''
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    code = post_data.get('code').strip()
    app_id = post_data.get('appId').strip()
    nickname = post_data.get('nickname').strip()
    image=post_data.get('image').strip()
    city=post_data.get('city').strip()
    country=post_data.get('country').strip()
    gender=post_data.get('gender')
    province=post_data.get('province').strip()
    if gender==1:
        gender='male'
    if gender==0:
        gender='female'
    response = {}
    if not code or not app_id:
        response['message'] = 'authorized failed, need entire authorization data.'
        response['code '] = ReturnCode.BROKEN_AUTHORIZED_DATA
        return JsonResponse(data=response, safe=False)

    data = c2s(app_id, code)
    openid = data.get('openid')

    print('get openid: ', openid)
    if not openid:
        response = wrap_json_response(code=ReturnCode.FAILED, message='auth failed')
        return JsonResponse(data=response, safe=False)

    request.session['open_id'] = openid
    request.session['is_authorized'] = True
    user=UserProfile.objects.filter(open_id=openid)

    if not user:
        r = requests.get(image)
        with open(Root_DIR + '/media/image/%s.png' % openid, 'wb') as f:
            f.write(r.content)
        image = 'image/%s.png' % openid
        new_user = UserProfile(open_id=openid, nickname=nickname,image=image,gender=gender,address=country+"\t"+province+"\t"+city,username=openid)
        print('new user: open_id: %s, nickname: %s' % (openid, nickname) )
        new_user.save()
        response = {"nick_name": new_user.nickname, "image": str(new_user.image), "code": ReturnCode.SUCCESS}
        print(response)
        return JsonResponse(data=response, safe=False)
    else:
        # TypeError: Object of type 'ImageFieldFile' is not JSON serializable
        # response={"nick_name":user[0].nickname,"image":user[0].image.path,"code":ReturnCode.SUCCESS}
        # path 是打印完整目录， str打印内容
        response={"nick_name":user[0].nickname,"image":str(user[0].image),"code":ReturnCode.SUCCESS}

        # response = wrap_json_response(code=ReturnCode.SUCCESS, message='{ "nick_name" success.')
        print(response)
        return JsonResponse(data=response, safe=False)

# 只有认证了，才可以获取open_id ,才可以知道是不是一个新用户，或者老用户
# 如果需要登陆，判断already ，如果没有就返回没等人，让其登入，如果登入就可以直接从session中获取open_id 然后
def authorize(request):
    return __authorize_by_code(request)


# 判断是否已经登陆
def get_status(request):
    print('call get_status function...')
    if already_authorized(request):
        data = {"is_authorized": 1}
    else:
        data = {"is_authorized": 0}
    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(response, safe=False)

def wxlogout(request):
    '''
    注销，小程序删除存储的Cookies
    '''
    request.session.clear()
    response = {}
    response['result_code'] = 0
    response['message'] = 'logout success.'
    return JsonResponse(response, safe=False)

# 通过modle创建的form表单验证，数据可以直接保存
class WXUserinfoView(View,CommonResponseMixin):
    def get(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(response, safe=False)
        open_id = request.session.get('open_id')
        user = UserProfile.objects.get(open_id=open_id)
        data = {}
        data['open_id'] = user.open_id
        data['data_joined'] = user.data_joined
        data['nickname'] = user.nickname
        data['birthday'] = user.birthday
        data['gender'] = user.gender
        data['address'] = user.address
        data['signature'] = user.signature
        print('data: ', data)
        response = CommonResponseMixin.wrap_json_response(code=ReturnCode.SUCCESS, data=data)
        return JsonResponse(response, safe=False)

    def post(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(response, safe=False)
        open_id = request.session.get('open_id')
        user = UserProfile.objects.get(open_id=open_id)
        # got str object
        received_body = request.body.decode('utf-8')
        received_body = eval(received_body)

        nickname = received_body.get('nickname')
        birthday = received_body.get('birthday')
        gender = received_body.get('gender')
        address = received_body.get('address')
        signature = received_body.get('signature')

        user.nickname = nickname
        user.birthday = birthday
        user.gender = gender
        user.address = address
        user.signature = signature

        user.save()
        message = 'modify user info success.'
        response = CommonResponseMixin.wrap_json_response(code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(response, safe=False)


class WXUploadImageView(View,CommonResponseMixin):
    def post(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(response, safe=False)
        open_id = request.session.get('open_id')
        user = UserProfile.objects.get(open_id=open_id)
        userImage = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        user.image=userImage
        user.save()
        response = wrap_json_response(code=ReturnCode.SUCCESS, message='头像修改成功')
        print(response)
        return JsonResponse(data=response, safe=False)


class WXMyFavWorksView(View,CommonResponseMixin):
    def get(self, request):
        # sort = request.GET['sort']
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(response, safe=False)
        open_id = request.session.get('open_id')
        user = UserProfile.objects.get(open_id=open_id)
        work_list = []
        fav_works = UserFavorite.objects.filter(user=user, fav_type=1).order_by("-add_time")
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
        work_list_=[]
        have_next=False
        for work in works:
            work_list_.append((work.id,str(work.image)))
        if works.has_next():
            have_next = True
        response = {"work_list":work_list_, "have_next":have_next, "code": ReturnCode.SUCCESS}
        print(response)
        return JsonResponse(data=response, safe=False)


class WXMyLoveWorksView(CommonResponseMixin, View):
    def get(self, request):
        # sort = request.GET['sort']
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(response, safe=False)
        open_id = request.session.get('open_id')
        user = UserProfile.objects.get(open_id=open_id)
        work_list = []
        fav_works = UserLove.objects.filter(user=user, love_type=1).order_by("-add_time")
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
        work_list_ = []
        have_next = False
        for work in works:
            work_list_.append((work.id, str(work.image)))
        if works.has_next():
            have_next = True
        response = {"work_list": work_list_, "have_next": have_next, "code": ReturnCode.SUCCESS}
        print(response)
        return JsonResponse(data=response, safe=False)


class WXMyWorksView(CommonResponseMixin, View):
    def get(self, request):
        # sort = request.GET['sort']
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(response, safe=False)
        open_id = request.session.get('open_id')
        user = UserProfile.objects.get(open_id=open_id)
        userworks_list = UserWorks.objects.filter(user=user).order_by("-add_time")
        works_list=[]
        for userworks in userworks_list:
            if userworks.works is not None:
                works_list.append(userworks.works)
            else:
                print(userworks.id+'userworks.works is None')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(works_list, 8)
        works = p.page(page)
        work_list_ = []
        have_next = False
        for work in works:
            work_list_.append((work.id, str(work.image)))
        if works.has_next():
            have_next = True
        response = {"work_list": work_list_, "have_next": have_next, "code": ReturnCode.SUCCESS}
        print(response)
        return JsonResponse(data=response, safe=False)



