from django.db import models
from datetime import datetime
from wanwenyc.settings import DJANGO_SERVER_YUMING

# Create your models here.
class Report(models.Model):
    testproject = models.CharField(max_length=50, default="", verbose_name=u"测试项目")
    testmodule = models.CharField(max_length=50, default="", verbose_name=u"项目模块")
    reportname = models.CharField(max_length=20, default="", verbose_name=u"测试执行开始时间串")
    reportfile = models.FileField(upload_to="report/%Y%m" , verbose_name=u"报告文件", max_length=1000)
    # reportimage = models.ImageField(upload_to="report/%Y%m/screenshots/",verbose_name=u"报告中错误截图",max_length=1000,height_field="image_height",width_field="image_width")   #图片类型，可以定义宽度（width_field）和高度（height_field）
    # image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="50")  #设置图片高度field
    # image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="50")   #设置图片宽度field
    add_time = models.DateTimeField(null=True, blank=True,auto_now_add=True,
                                    verbose_name=u"添加时间")  # datetime.now记录实例化时间，datetime.now()记录模型创建时间,auto_now_add=True是指定在数据新增时, 自动写入时间
    update_time = models.DateTimeField(null=True, blank=True,auto_now=True,
                                    verbose_name=u"更新时间")  # datetime.now记录实例化时间，datetime.now()记录模型创建时间，auto_now=True是无论新增还是更新数据, 此字段都会更新为当前时间

    class Meta:
        verbose_name = u"报告记录"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.reportname

    def go_to(self):   #定义点击后跳转到某一个地方（可以加html代码）
        from django.utils.safestring import mark_safe   #调用mark_safe这个函数，django可以显示成一个文本，而不是html代码
        return mark_safe("<a href='{}/media/{}'>{}</a>".format(DJANGO_SERVER_YUMING,self.reportfile,self.reportfile))
        # return  "<a href='http://192.168.212.194:9002/testcase/{}/'>跳转</a>".format(self.id)

    go_to.short_description = u"报告文件"   #为go_to函数名个名字
