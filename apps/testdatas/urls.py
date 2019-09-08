# _*_ coding:utf-8 _*_

__author__ = 'bobby'
__date__ = '2018/5/15 18:21'
from django.urls import  path

# from .views import TestCaseView, DisplayTestCaseView,MoreTestCaseView,AllTestCaseSiderView,SiderCaseDisplayView,SiderCaseDetailsView   #导入TestCaseView
from .views import ClickAndBackView   #导入ClickAndBackView


urlpatterns = [
    #相同参数的路径名一定不能一样。比如copy/<path:testcase_id>/与<path:testcase_id>/不能并列存在
    path('copy/<path:clickandback_id>/', ClickAndBackView.as_view(), name="click_and_back_id"),  # 配置复制新增测试用例url,namespace指明命名空间，用命名空间做限定
]

app_name = 'clickandback'