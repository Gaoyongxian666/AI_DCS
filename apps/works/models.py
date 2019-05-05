# from datetime import datetime
from django.utils import timezone as datetime
from django.db import models

# Create your models here.

# desc = UEditorField(verbose_name=u"机构描述",width=900, height=300, imagePath="org/ueditor/",
    #                                      filePath="org/ueditor/", default='')
    # 关于富文本编辑器，django直接集成的都是只能在后台直接用的
    # 当然前端是可以直接显示出来的

class Works(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"作品名称")
    tag = models.CharField(max_length=10, verbose_name=u"作品标签")
    love_nums = models.IntegerField(default=0, verbose_name=u"点赞数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    download_nums = models.IntegerField(default=0, verbose_name=u"下载数")
    image = models.ImageField(upload_to="works/%Y/%m", verbose_name=u"作品", max_length=100)
    desc = models.CharField(max_length=1500, verbose_name=u"说明")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"作品"
        verbose_name_plural = verbose_name

    # def get_teacher_nums(self):
    #     #获取课程机构的教师数量
    #     return self.teacher_set.all().count()

    def __str__(self):
        return self.name

