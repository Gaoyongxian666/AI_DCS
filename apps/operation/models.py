# from datetime import datetime
from django.utils import timezone as datetime
from django.db import models

# Create your models here.
from users.models import UserProfile
from works.models import Works


class WorksComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户",on_delete=models.CASCADE)
    works = models.ForeignKey(Works, verbose_name=u"作品",on_delete=models.CASCADE)
    comments = models.CharField(max_length=200, verbose_name=u"评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"作品评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        str1=str(self.user)+"对作品："+str(self.works)+"的评论"
        return str1


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户",on_delete=models.CASCADE)
    # on_delet 外键 https://www.cnblogs.com/phyger/p/8035253.html
    fav_id = models.IntegerField(default=0, verbose_name=u"作品id")
    fav_type = models.IntegerField(choices=((1,"作品"),(2,'作者')), default=1, verbose_name=u"收藏类型")
    # 'choices' must be an iterable containing (actual value, human readable name) tuples
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        str1=str(self.user)+"收藏的作品id："+str(self.fav_id)
        return str1


class UserLove(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户",on_delete=models.CASCADE)
    # on_delet 外键 https://www.cnblogs.com/phyger/p/8035253.html
    love_id = models.IntegerField(default=0, verbose_name=u"作品id")
    love_type = models.IntegerField(choices=((1,"作品"),(2,'作者')), default=1, verbose_name=u"点赞类型")
    # 'choices' must be an iterable containing (actual value, human readable name) tuples
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户点赞"
        verbose_name_plural = verbose_name

    def __str__(self):
        str1=str(self.user)+"点赞的作品id："+str(self.fav_id)
        return str1

class UserWorks(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户",on_delete=models.CASCADE)
    works = models.ForeignKey(Works, verbose_name=u"作品",on_delete=models.CASCADE,blank=True, null=True)
    material = models.ImageField(upload_to="material/resource/%Y/%m", verbose_name=u"用户上传的资源文件", max_length=100,default="image/default.png")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户作品"
        verbose_name_plural = verbose_name

    def __str__(self):
        # 可以返回字符串，self.user是UserProfile类型的不能与str直接加减
        str1=str(self.user)+"的作品："+str(self.works)
        return str1

class UserMessage(models.Model):
    # 因为我们的消息有两种:发给全员和发给某一个用户。
    # 所以如果使用外键，每个消息会对应要有用户。很难实现全员消息。

    # 机智版 为0发给所有用户，不为0就是发给用户的id
    user = models.IntegerField(default=0, verbose_name=u"接收用户")
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        # 可以返回字符串，self.user是UserProfile类型的不能与str直接加减
        str1 = str(self.user) + "的消息：" + str(self.message)
        return str1
