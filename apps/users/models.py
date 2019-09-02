from datetime import datetime   #系统的包放在最上面

from django.db import models   #第二个级别的就是第三方包
from django.contrib.auth.models import AbstractUser   #导入django的用户模块

#第三个就是我们自己创建的包
# Create your models here.


class UserProfile(AbstractUser):#继承django的user模块，其中包含的字段都有，以下是新增的字段
    """
    用户
    """
    china_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")  #null=True.表示实例化的时候可以为空，blank=True表示填写的内容可以为空
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", u"女")), default="female", verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    id_number= models.CharField(null=True, blank=True, max_length=20, verbose_name="身份证号码")

    # datetime.now记录实例化时间，datetime.now()记录模型创建时间,auto_now_add=True是指定在数据新增时, 自动写入时间
    add_time = models.DateTimeField(null=True, blank=True, auto_now_add=True,verbose_name=u"添加时间")
    # datetime.now记录实例化时间，datetime.now()记录模型创建时间，auto_now=True是无论新增还是更新数据, 此字段都会更新为当前时间
    update_time = models.DateTimeField(default=datetime.now, null=True, blank=True,verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"用户"
        verbose_name_plural =verbose_name

    def __str__(self):#重载函数
        return self.username
