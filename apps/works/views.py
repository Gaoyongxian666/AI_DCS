import json
import os
from AIDCS.tasks import do_painter,do_figure,do_ink,do_sketch,do_style,do_color

from django.core.files.base import ContentFile
from django.core.paginator import Paginator, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.safestring import mark_safe
from django.views import View
from AI_DCS.settings import MEDIA_URL, Active_IP
from operation.models import UserFavorite, UserLove, UserWorks, WorksComments
from utils.mixin_utils import LoginRequiredMixin
from works.models import Works


class WorksListView(View):
    def get(self, request):
        all_works = Works.objects.all().order_by("-add_time")
        try:
            sort = request.GET['sort']
        except MultiValueDictKeyError:
            sort="6"

        intro='''<h3>Chinese Brush Painting </h3>
                       <p>风景画智能转化成中国风水墨画</p>
                       <p>“给我一张您手中的风景美图，</p>
                       <p>还您一场绮丽的水墨烟雨。”</p>    
                '''

        if sort == "0":
            all_works = all_works.filter(tag__icontains="logo生成")
            intro='''
            <h3>Splendid LOGO</h3>
                       <p>一键logo生成</p>
                       <p>这里是一口神奇的坩埚</p>
                       <p>加一点流动的时间</p>
                       <p>加一朵心头的花儿</p>
                       <p>倒入满满的创意</p>
                       <p>念动神秘的咒语</p>
                       <p>嘭！</p>
                       <p>一个logo诞生啦！</p>'''
        if sort == "1":
            all_works = all_works.filter(tag__icontains="线稿上色")
            intro = '''<h3>Colourful Line art </h3>
                       <p>“我画了一个萌萌哒的女孩子哦！”</p>
                       <p>“头发什么颜色好呢？</p>
                       <p>那眼睛搭配什么颜色？</p>
                       <p>白皮还是黑皮……”</p>
                       <p>请把线稿给我</p>
                       <p>给您完美的上色搭配</p>'''
        if sort == "2":
            all_works = all_works.filter(tag__icontains="风格生成")
            intro = '''<h3>Various Style </h3>
                       <p>图片风格化</p>
                       <p>一张图片，千般风情</p>
                       <p>“我喜欢厚涂风格，是化不开的重彩，一笔一笔。”</p>
                       <p>“我喜欢魔幻风格，色彩靓丽且多变，一层一层。”</p>
                       <p>“我喜欢现代风格，仿佛剥落的墙漆，一块一块。”</p>
                       <p>……</p>
                       <p>小孩子才做选择，我全都要。</p>'''
        if sort == "3":
            all_works = all_works.filter(tag__icontains="灰度图上色")
            intro = '''<h3>Gray Scale Image </h3>
                       <p>“加一个色彩平衡图层？</p>
                       <p>还有色相饱和度也需要调？</p>
                       <p>那亮度对比度呢？”</p>
                       <p>这些问题通通抛在脑后吧</p>
                       <p>给我一张灰度图</p>
                       <p>完全私人订制上色哟!</p>'''
        if sort == "4":
            all_works = all_works.filter(tag__icontains="水墨画生成")
            intro = '''<h3>Splendid LOGO</h3>
                                   <p>一键logo生成</p>
                                   <p>这里是一口神奇的坩埚</p>
                                   <p>加一点流动的时间</p>
                                   <p>加一朵心头的花儿</p>
                                   <p>倒入满满的创意</p>
                                   <p>念动神秘的咒语</p>
                                   <p>嘭！</p>
                                   <p>一个logo诞生啦！</p>'''
        if sort == "5":
            all_works = all_works.filter(tag__icontains="生成动漫")
            intro = '''<h3>Figure Cartoon Transition </h3>
                       <p>人物照片转换成漫画</p>
                       <p>二次元酷哥？</p>
                       <p>圆嘟嘟可爱小萝莉？</p>
                       <p>闪亮亮的日系插画风小姐姐？</p>
                       <p>给我一张照片</p>
                       <p>下一个打破次元壁的俊男靓女就是您啦</p>'''

        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_works = all_works.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_works, 9)
        works = p.page(page)

        # 下面这些都是针对p 就是分类器对象而言的
        # 把对象p传到前端也是可以使用的
        ## 要分页的总对象数paginator.count 7
        # 每一页的对象以列表的形式 paginator.object_list ['post1', 'post2', 'post3', 'post4', 'post5', 'post6', 'post7']
        ## 总共可以分页数，也就是总共可以分成多少页 paginator.num_pages 3
        ## 页码取值范围 paginator.page_range 相当于range(1, 4)
        ## 每页几个对象 paginator.per_page 3
        ## 取第2页， 或者第N页`paginator.page(N)` page2 = paginator.page(2)

        # django模板的加减 乘除
        # Django模版加法：{{value | add: 10}}
        # { % widthratio 5 1 100 %} widthratio需要三个参数，它会使用 参数1 / 参数2 * 参数3
        # 如果在if中比较的话 大于号 注意左右要加空格

        # 模板筛选器 https://www.cnblogs.com/haoshine/p/6014500.html
        # chua
        return render(request, 'moreWorks.html', {
            "all_works": works,
            "sort": sort,
            "page": page,
            "p": p,
            "jianjie":mark_safe(intro)
        })




class WorksDetailView(View):
    def get(self, request, work_id):
        username="未知的"
        task_id="0"
        if work_id==0:
            print(request.GET["task_id"])
            task_id=request.GET["task_id"]
            work= Works.objects.get(task_id=task_id)
            userworks = UserWorks.objects.filter(works=work)
        else:
            print(work_id)
            work = Works.objects.get(id=int(work_id))
            userworks = UserWorks.objects.filter(works=work)
        if userworks:
            muser = userworks[0].user
            username = muser.username



        # user 不能用
        try:

            if request.user.image:
                user_image=request.user.image
            else:
                user_image="works/2018/10/person.png"
            if request.user.nick_name == "":
                user_name=request.user.username
            elif request.user.nick_name:
                user_name=request.user.nick_name
            else:
                user_name="请登陆"
        except AttributeError:
            user_image = "works/2018/10/person.png"
            user_name = "请登陆"

        has_fav_work = False
        has_love_work = False

        # 'bool' object is not callable 不能使用request.user.is_authenticated():
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=work.id, fav_type=1):
                has_fav_work = True
            if UserLove.objects.filter(user=request.user, love_id=work.id, love_type=1):
                has_love_work = True

        all_comments = WorksComments.objects.filter(works=work).order_by("-id")
        comment_num=all_comments.count()
        user_list=[]
        for comment in all_comments:
            user_list.append(comment.user)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1


        p = Paginator(all_comments, 9)
        comments = p.page(page)


        return render(request, "worksDetails.html", {
            "task_id":task_id,
            "userworks":userworks[0],
            "work": work,
            "user_image":mark_safe(user_image),
            "has_love_work": has_love_work,
            "has_fav_work": has_fav_work,
            "username": username,
            'user_name': user_name,
            "all_comments":comments,
            "comments_num":comment_num,
            "page": page,
            "p":p
        })



# 添加评论
class AddComentsView(View):

    def post(self, request):
        if not request.user.is_authenticated:
            #判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        work_id = request.POST.get("work_id", 0)
        comments = request.POST.get("comments", "")
        if int(work_id) >0 and comments:
            work_comments = WorksComments()
            work = Works.objects.get(id=int(work_id))
            work_comments.works = work
            work_comments.comments = comments
            work_comments.user = request.user
            work_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


# 收藏
class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                # 收藏作品,所以在作品的点赞数上见一
                work = Works.objects.get(id=int(fav_id))
                work.fav_nums -= 1
                if work.fav_nums < 0:
                    work.fav_nums = 0
                work.save()
            data = {"status": "success", "msg": "收藏", "fav_num": work.fav_nums}
            return HttpResponse(json.dumps(data), content_type="application/json")
            # return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            # 判断非正常请求,与默认有关
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    work = Works.objects.get(id=int(fav_id))
                    work.fav_nums += 1
                    work.save()
                # return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
                data = {"status": "success", "msg":"已收藏","fav_num": work.fav_nums}
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')

# 点赞
class AddLoveView(View):
    def post(self, request):
        love_id = request.POST.get('love_id', 0)
        love_type = request.POST.get('love_type', 0)
        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserLove.objects.filter(user=request.user, love_id=int(love_id), love_type=int(love_type))
        if exist_records:
            # 如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            if int(love_type) == 1:
                # 收藏作品,所以在作品的点赞数上见一
                work = Works.objects.get(id=int(love_id))
                work.love_nums -= 1
                if work.love_nums < 0:
                    work.love_nums = 0
                work.save()
            data = {"status": "success", "msg":"点赞","love_num": work.love_nums}
            return HttpResponse(json.dumps(data), content_type="application/json")


        else:
            user_love = UserLove()
            # 判断非正常请求,与默认有关
            if int(love_id) > 0 and int(love_type) > 0:
                user_love.user = request.user
                user_love.love_id = int(love_id)
                user_love.love_type = int(love_type)
                user_love.save()

                if int(love_type) == 1:
                    work = Works.objects.get(id=int(love_id))
                    work.love_nums += 1
                    work.save()
                data = {"status": "success", "msg": "已点赞", "love_num": work.love_nums}
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                return HttpResponse('{"status":"fail", "msg":"点赞出错"}', content_type='application/json')


# 下载
class DownloadView(View):
    def get(self, request, work_id):
        work = Works.objects.get(id=int(work_id))
        work.download_nums += 1
        work.save()
        # file = open(work.image.path, 'rb')
        # 在后台 work.image 是image文件类型的
        response = FileResponse(work.image)
        response['Content-Type'] = 'application/octet-stream'
        # response['Content-Disposition'] = 'attachment;filename=works.png'
        filename = work.name + ".png"
        response['Content-Disposition'] = 'attachment; filename=' + filename.encode('utf-8').decode('ISO-8859-1')
        return response
        # 在后台把文件名先encode成bytes，再判断浏览器，根据不同的浏览器用相应的编码decode一下就好了
        # 例如浏览器是ff，后台编码是utf - 8
        # response['Content-Disposition'] = 'attachment; filename=' + filename.encode('utf-8).decode('
        # ISO - 8859 - 1
        # ')
        # 就ok了
        #
        # 常用浏览器解析格式。
        #
        # IE浏览器，采用URLEncoder编码
        # Opera浏览器，采用filename * 方式
        # Safari浏览器，采用ISO编码的中文输出
        # Chrome浏览器，采用Base64编码或ISO编码的中文输出
        # FireFox浏览器，采用Base64或filename * 或ISO编码的中文输出
    def post(self, request):
        download_id = request.POST.get('download_id', 0)
        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        work = Works.objects.get(id=int(download_id))
        download_num=work.download_nums+1
        data = {"status": "success", "msg":"下载","download_num": download_num}
        # print(download_num)
        return HttpResponse(json.dumps(data), content_type="application/json")



class GenerateGrayView(LoginRequiredMixin, View):
    def post(self, request):
        work = Works()
        userworks = UserWorks()

        name = request.POST.get('name', "未命名作品")
        if name== '':
            name="未命名作品"
        desc = request.POST.get('desc', "这篇作品还没有作品描述")
        if desc=='':
            desc="这篇作品还没有作品描述"
        userImage = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None


        tag="灰度图上色"

        userworks.user = request.user
        userworks.material = userImage
        userworks.save()


        material_path=userworks.material.path

        Base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        img_path = Base_dir + "/static/img/1.jpg"

        userGenerateGray = ContentFile(open(Base_dir + "/static/img/1.jpg", "rb").read())

        # 保存生成的作品
        work.tag = tag
        work.name = name
        work.desc = desc
        work.image.save("work.jpg", userGenerateGray)
        work.save()

        # 灰度 colornet 线稿 Painter 风格 StyleTransfer 生成动漫 Figure 水墨画生成 Chinese
        # 线稿生成 sketch

        # Main.choose(model_name="Colornet",content=material_path,output=work.image.path,style_model = '/home/ai/AI_DCS/AIDCS/StyleTransfer/models/wave.ckpt')



        userworks.works = work
        userworks.save()

        task_name = do_color.delay(content=material_path, output=work.image.path)
        work.task_id = task_name
        work.save()

        data = {"status": "success", "task_id": str(task_name)}

        return HttpResponse(json.dumps(data), content_type="application/json")
    def get(self, request):
        return render(request, template_name="functionGray.html")

class GenerateLineArtView(LoginRequiredMixin, View):
    def post(self, request):
        work = Works()
        userworks = UserWorks()

        name = request.POST.get('name', "未命名作品")
        if name== '':
            name="未命名作品"
        desc = request.POST.get('desc', "这篇作品还没有作品描述")
        if desc=='':
            desc="这篇作品还没有作品描述"
        userImage = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None

        tag="线稿上色"



        userworks.user = request.user
        userworks.material = userImage
        userworks.save()


        material_path=userworks.material.path

        Base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        img_path=Base_dir+"/static/img/1.jpg"
        print(img_path)

        defult= ContentFile(open(Base_dir+"/static/img/1.jpg", "rb").read())

        # 保存生成的作品
        work.tag = tag
        work.name = name
        work.desc = desc
        work.image.save("work.jpg", defult)





        #

        # Main.choose(model_name="Painter",content=material_path,output=work.image.path)

        userworks.works = work
        userworks.save()
        # 这是同步，必须要结果，服务必须开这

        task_name = do_painter.delay(content=material_path, output=work.image.path)
        work.task_id = task_name
        work.save()

        data={"status":"success","task_id": str(task_name)}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def get(self, request):
        return render(request, template_name="functionLineArt.html")

class GenerateFigureView(LoginRequiredMixin, View):
    def post(self, request):
        work = Works()
        userworks = UserWorks()

        name = request.POST.get('name', "未命名作品")
        if name== '':
            name="未命名作品"
        desc = request.POST.get('desc', "这篇作品还没有作品描述")
        if desc=='':
            desc="这篇作品还没有作品描述"
        userImage = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None


        tag="生成动漫"

        userworks.user = request.user
        userworks.material = userImage
        userworks.save()


        material_path=userworks.material.path

        Base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        img_path = Base_dir + "/static/img/1.jpg"

        userGenerateGray = ContentFile(open(Base_dir + "/static/img/1.jpg", "rb").read())

        # 保存生成的作品
        work.tag = tag
        work.name = name
        work.desc = desc
        work.image.save("work.jpg", userGenerateGray)
        work.save()

        # 灰度 colornet 线稿 Painter 风格 StyleTransfer 生成动漫 Figure 水墨画生成 Chinese
        # 线稿生成 sketch
        # Main.choose(model_name="Figure",content=material_path,output=work.image.path,style_model = '/home/ai/AI_DCS/AIDCS/StyleTransfer/models/wave.ckpt')



        userworks.works = work
        userworks.save()

        userworks.works = work
        userworks.save()
        # 这是同步，必须要结果，服务必须开这

        task_name = do_figure.delay(content=material_path, output=work.image.path)
        work.task_id = task_name
        work.save()

        data = {"status": "success", "task_id": str(task_name)}



        return HttpResponse(json.dumps(data), content_type="application/json")
    def get(self, request):
        return render(request, template_name="functionComic.html")

class GenerateChineseView(LoginRequiredMixin, View):
    def post(self, request):
        work = Works()
        userworks = UserWorks()

        name = request.POST.get('name', "未命名作品")
        if name== '':
            name="未命名作品"
        desc = request.POST.get('desc', "这篇作品还没有作品描述")
        if desc=='':
            desc="这篇作品还没有作品描述"
        userImage = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None


        tag="水墨画生成"

        userworks.user = request.user
        userworks.material = userImage
        userworks.save()


        material_path=userworks.material.path

        Base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        img_path = Base_dir + "/static/img/1.jpg"

        userGenerateGray = ContentFile(open(Base_dir + "/static/img/1.jpg", "rb").read())
        # 保存生成的作品
        work.tag = tag
        work.name = name
        work.desc = desc
        work.image.save("work.jpg", userGenerateGray)
        work.save()

        # 灰度 colornet 线稿 Painter 风格 StyleTransfer 生成动漫 Figure 水墨画生成 Chinese
        # 线稿生成 sketch
        # Main.choose(model_name="Chinese",content=material_path,output=work.image.path,style_model = '/home/ai/AI_DCS/AIDCS/StyleTransfer/models/wave.ckpt')



        userworks.works = work
        userworks.save()
        userworks.works = work
        userworks.save()
        # 这是同步，必须要结果，服务必须开这

        task_name = do_ink.delay(content=material_path, output=work.image.path)
        work.task_id = task_name
        work.save()

        data = {"status": "success", "task_id": str(task_name)}

        return HttpResponse(json.dumps(data), content_type="application/json")
    def get(self, request):
        return render(request, template_name="functionChinese.html")

class GenerateLineView(LoginRequiredMixin, View):
    def post(self, request):
        work = Works()
        userworks = UserWorks()

        name = request.POST.get('name', "未命名作品")
        if name== '':
            name="未命名作品"
        desc = request.POST.get('desc', "这篇作品还没有作品描述")
        if desc=='':
            desc="这篇作品还没有作品描述"
        userImage = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None

        tag="生成线稿"



        userworks.user = request.user
        userworks.material = userImage
        userworks.save()


        material_path=userworks.material.path

        Base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        img_path = Base_dir + "/static/img/1.jpg"

        userGenerateGray = ContentFile(open(Base_dir + "/static/img/1.jpg", "rb").read())
        # 保存生成的作品
        work.tag = tag
        work.name = name
        work.desc = desc
        work.image.save("work.jpg", userGenerateGray)
        work.save()

        # Main.choose(model_name="Sketch",content=material_path,output=work.image.path)

        userworks.works = work
        userworks.save()

        userworks.works = work
        userworks.save()
        # 这是同步，必须要结果，服务必须开这

        task_name = do_sketch.delay(content=material_path, output=work.image.path)
        work.task_id = task_name
        work.save()

        data = {"status": "success", "task_id": str(task_name)}

        return HttpResponse(json.dumps(data), content_type="application/json")

    def get(self, request):
        return render(request, template_name="functionLine.html")

class GenerateStyleView(LoginRequiredMixin, View):
    def post(self, request):
        work = Works()
        userworks = UserWorks()

        name = request.POST.get('name', "未命名作品")
        if name== '':
            name="未命名作品"
        desc = request.POST.get('desc', "这篇作品还没有作品描述")
        if desc=='':
            desc="这篇作品还没有作品描述"
        userImage = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None


        tag="风格生成"

        style = request.POST.get('style', "0")


        userworks.user = request.user
        userworks.material = userImage
        userworks.save()


        material_path=userworks.material.path

        Base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        img_path = Base_dir + "/static/img/1.jpg"

        userGenerateGray = ContentFile(open(Base_dir + "/static/img/1.jpg", "rb").read())

        # 保存生成的作品
        work.tag = tag
        work.name = name
        work.desc = desc
        work.image.save("work.jpg", userGenerateGray)
        work.save()

        # 灰度 colornet 线稿 Painter 风格 StyleTransfer 生成动漫 Figure 水墨画生成 Chinese
        # 线稿生成 sketch

        if style=="0":
            style_model="/home/ai/AI_DCS/AIDCS/StyleTransfer/models/wave.ckpt"
        if style=="1":
            style_model="/home/ai/AI_DCS/AIDCS/StyleTransfer/models/la_muse.ckpt"
        if style=="2":
            style_model="/home/ai/AI_DCS/AIDCS/StyleTransfer/models/rain_princess.ckpt"
        if style=="3":
            style_model="/home/ai/AI_DCS/AIDCS/StyleTransfer/models/shipwreck.ckpt"
        if style=="4":
            style_model="/home/ai/AI_DCS/AIDCS/StyleTransfer/models/the_scream.ckpt"
        if style=="5":
            style_model="/home/ai/AI_DCS/AIDCS/StyleTransfer/models/udnie.ckpt"


        # Main.choose(model_name="StyleTransfer",content=material_path,output=work.image.path,style_model = style_model)



        userworks.works = work
        userworks.save()
        userworks.works = work
        userworks.save()
        # 这是同步，必须要结果，服务必须开这

        task_name = do_style.delay(content=material_path, output=work.image.path,style_model = style_model)
        work.task_id = task_name
        work.save()

        data = {"status": "success", "task_id": str(task_name)}

        data={"status":"success","image_path": Active_IP+MEDIA_URL+str(work.image)}
        return HttpResponse(json.dumps(data), content_type="application/json")
    def get(self, request):
        return render(request, template_name="functionStyle.html")

class GenerateLogoView(LoginRequiredMixin, View):
    def post(self, request):
        work = Works()
        userworks = UserWorks()

        name = request.POST.get('name', "未命名作品")
        if name== '':
            name="未命名作品"
        desc = request.POST.get('desc', "这篇作品还没有作品描述")
        if desc=='':
            desc="这篇作品还没有作品描述"
        userImage = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None


        tag="灰度图上色"

        userworks.user = request.user
        userworks.material = userImage
        userworks.save()


        material_path=userworks.material.path

        Base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        img_path = Base_dir + "/static/img/1.jpg"

        userGenerateGray = ContentFile(open(Base_dir + "/static/img/1.jpg", "rb").read())

        # 保存生成的作品
        work.tag = tag
        work.name = name
        work.desc = desc
        work.image.save("work.jpg", userGenerateGray)
        work.save()

        # 灰度 colornet 线稿 Painter 风格 StyleTransfer 生成动漫 Figure 水墨画生成 Chinese
        # 线稿生成 sketch
        # Main.choose(model_name="Colornet",content=material_path,output=work.image.path,style_model = '/home/ai/AI_DCS/AIDCS/StyleTransfer/models/wave.ckpt')



        userworks.works = work
        userworks.save()

        data={"status":"success","image_path": Active_IP+MEDIA_URL+str(work.image)}
        return HttpResponse(json.dumps(data), content_type="application/json")
    def get(self, request):
        return render(request, template_name="functionLogo.html")



