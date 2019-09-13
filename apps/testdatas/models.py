from datetime import datetime   #系统的包放在最上面

from django.db import models   #第二个级别的就是第三方包
from django.contrib.auth import  get_user_model  #导入get_user_model

from wanwenyc.settings import DJANGO_SERVER_YUMING

#第三个就是我们自己创建的包
User = get_user_model()  #get_user_model() 函数直接返回User类，找的是settings.AUTH_USER_MODEL变量的值
# Create your models here.


class ClickAndBack(models.Model):#继承django的Model模块
    """
    点击滑动返回测试场景测试数据
    """
    test_project = models.CharField(max_length=100, default="", verbose_name=u"测试项目")
    test_module = models.CharField(max_length=100, default="",null=True, blank=True, verbose_name=u"测试模块")
    test_page = models.CharField(max_length=100, default="", verbose_name=u"测试页面")
    test_case_title = models.CharField(max_length=200, default="", verbose_name=u"测试内容的名称")
    is_run_case = models.BooleanField(default=True,verbose_name=u"是否运行")
    current_page_click_ele_find = models.CharField(max_length=100, default="xpath",
                                                    verbose_name=u"当前页面要点击元素查找风格",
                                                    help_text=u"元素查找风格：id、name、class_name、tag_name、"
                                                              u"link_text、partial_link_text、css_selector、xpath")
    current_page_click_ele_find_value = models.CharField(max_length=1000, default="",
                                                         verbose_name=u"当前页面要点击元素查找风格的确切值")
    is_new = models.BooleanField(default=False, verbose_name=u"是否新窗口")
    next_page_check_ele_find= models.CharField(max_length=100,
                                             default="xpath", verbose_name=u"下一页面标识元素查找风格",
                                             help_text=u"元素查找风格：id、name、class_name、tag_name、"
                                                       u"link_text、partial_link_text、css_selector、xpath")
    next_page_check_ele_find_value = models.CharField(max_length=1000, default="",
                                                         verbose_name=u"下一页面要点击元素查找风格的确切值")
    case_counts = models.IntegerField(default="1",verbose_name="用例循环次数",help_text=u"用例循环次数，请填写数字，"
                                                                   u"例如：1、2、3")
    depend_case = models.ForeignKey('self', default="", null=True, blank=True,
                                   verbose_name=u"依赖的前置用例",on_delete=models.PROTECT)
    write_user = models.ForeignKey(User,related_name="writeuser",null=True, blank=True,
                                   verbose_name=u"添加用例人", on_delete=models.PROTECT)

    # datetime.now记录实例化时间，datetime.now()记录模型创建时间,auto_now_add=True是指定在数据新增时, 自动写入时间
    add_time = models.DateTimeField(null=True, blank=True, auto_now_add=True,verbose_name=u"添加时间")
    # datetime.now记录实例化时间，datetime.now()记录模型创建时间，auto_now=True是无论新增还是更新数据, 此字段都会更新为当前时间
    update_time = models.DateTimeField(default=datetime.now, null=True, blank=True,verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"点击场景"
        verbose_name_plural = verbose_name

    def __str__(self):#重载函数
        return self.test_case_title

    def go_to(self):   #定义点击后跳转到某一个地方（可以加html代码）
        from django.utils.safestring import mark_safe   #调用mark_safe这个函数，django可以显示成一个文本，而不是html代码
        return mark_safe("<a href='{}/clickandback/copy/{}/'>复制新加</a>".format(DJANGO_SERVER_YUMING,self.id))
        # return  "<a href='http://192.168.212.194:9002/testcase/{}/'>跳转</a>".format(self.id)

    go_to.short_description = u"复制新加"   #为go_to函数名个名字



class NewAddAndCheck(models.Model):#继承django的Model模块
    """
    新增数据场景
    """
    test_project = models.CharField(max_length=100, default="", verbose_name=u"测试项目")
    test_module = models.CharField(max_length=100, default="",null=True, blank=True, verbose_name=u"测试模块")
    test_page = models.CharField(max_length=100, default="", verbose_name=u"测试页面")
    test_case_title = models.CharField(max_length=200, default="", verbose_name=u"测试内容的名称")
    is_run_case = models.BooleanField(default=True,verbose_name=u"是否运行")
    depend_click_case = models.ForeignKey(ClickAndBack, default="", null=True, blank=True,
                                   verbose_name=u"依赖的点击场景的用例",on_delete=models.PROTECT)



    confirm_ele_find = models.CharField(max_length=100, default="xpath",verbose_name=u"确定按钮查找风格",
                                        help_text=u"元素查找风格：id、name、class_name、tag_name、"
                                                  u"link_text、partial_link_text、css_selector、xpath")
    confirm_ele_find_value = models.CharField(max_length=1000, default="",
                                                         verbose_name=u"确定按钮查找风格的确切值")
    is_click_cancel = models.BooleanField(default=False,verbose_name=u"是否点击取消按钮")
    cancel_ele_find = models.CharField(max_length=100, default="xpath", null=True, blank=True,
                                       verbose_name=u"取消按钮查找风格",
                                       help_text=u"元素查找风格：id、name、class_name、tag_name、"
                                                 u"link_text、partial_link_text、css_selector、xpath")
    cancel_ele_find_value = models.CharField(max_length=1000, default="",null=True, blank=True,
                                                         verbose_name=u"取消按钮查找风格的确切值")
    case_counts = models.IntegerField(default="1",verbose_name="循环次数",help_text=u"循环次数，请填写数字，"
                                                                   u"例如：1、2、3")
    write_user = models.ForeignKey(User,null=True, blank=True,verbose_name=u"添加人", on_delete=models.PROTECT)

    # datetime.now记录实例化时间，datetime.now()记录模型创建时间,auto_now_add=True是指定在数据新增时, 自动写入时间
    add_time = models.DateTimeField(null=True, blank=True, auto_now_add=True,verbose_name=u"添加时间")
    # datetime.now记录实例化时间，datetime.now()记录模型创建时间，auto_now=True是无论新增还是更新数据, 此字段都会更新为当前时间
    update_time = models.DateTimeField(default=datetime.now, null=True, blank=True,verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"新增场景"
        verbose_name_plural = verbose_name

    def __str__(self):#重载函数
        return self.test_case_title



class InputTapInputText(models.Model):
    newaddandcheck = models.ForeignKey(NewAddAndCheck,default="", null=True, blank=True,
                                   verbose_name=u"依赖的添加场景",on_delete=models.PROTECT)

    input_ele_find = models.CharField(max_length=100, default="xpath",verbose_name=u"输入框查找风格",
                                        help_text=u"元素查找风格：id、name、class_name、tag_name、"
                                                  u"link_text、partial_link_text、css_selector、xpath")
    input_ele_find_value = models.CharField(max_length=1000, default="",
                                                         verbose_name=u"输入框查找风格的确切值")
    input_text = models.CharField(max_length=300,default="",verbose_name=u"输入框中要输入的内容")
    # datetime.now记录实例化时间，datetime.now()记录模型创建时间,auto_now_add=True是指定在数据新增时, 自动写入时间
    add_time = models.DateTimeField(null=True, blank=True, auto_now_add=True,verbose_name=u"添加时间")
    # datetime.now记录实例化时间，datetime.now()记录模型创建时间，auto_now=True是无论新增还是更新数据, 此字段都会更新为当前时间
    update_time = models.DateTimeField(default=datetime.now, null=True, blank=True,verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"新增输入框及输入内容"
        verbose_name_plural = verbose_name

    def __str__(self):#重载函数
        return self.input_ele_find_value


class SelectTapSelectOption(models.Model):
    newaddandcheck = models.ForeignKey(NewAddAndCheck,default="", null=True, blank=True,
                                   verbose_name=u"依赖的添加场景",on_delete=models.PROTECT)

    select_ele_find = models.CharField(max_length=100, default="xpath",verbose_name=u"选项框的查找风格",
                                        help_text=u"元素查找风格：id、name、class_name、tag_name、"
                                                  u"link_text、partial_link_text、css_selector、xpath")
    select_ele_find_value = models.CharField(max_length=1000, default="",
                                                         verbose_name=u"选项框查找风格的确切值")
    select_option_ele_find = models.CharField(max_length=100, default="xpath",verbose_name=u"选项的查找风格",
                                        help_text=u"元素查找风格：id、name、class_name、tag_name、"
                                                  u"link_text、partial_link_text、css_selector、xpath")
    select_option_ele_find_value = models.CharField(max_length=1000, default="",
                                                         verbose_name=u"选项查找风格的确切值")
    # datetime.now记录实例化时间，datetime.now()记录模型创建时间,auto_now_add=True是指定在数据新增时, 自动写入时间
    add_time = models.DateTimeField(null=True, blank=True, auto_now_add=True,verbose_name=u"添加时间")
    # datetime.now记录实例化时间，datetime.now()记录模型创建时间，auto_now=True是无论新增还是更新数据, 此字段都会更新为当前时间
    update_time = models.DateTimeField(default=datetime.now, null=True, blank=True,verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"新增选项框及选项内容"
        verbose_name_plural = verbose_name

    def __str__(self):#重载函数
        return self.select_ele_find_value
