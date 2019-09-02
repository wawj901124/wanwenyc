import unittest
# ----------------------------------------------------------------------
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wanwenyc.settings")
django.setup()
# ----------------------------------------------------------------------
#独运行某一个py文件时会出现如下错误：django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.，以上内容可以解决此问题,加载django中的App
import ddt

from WWTest.autotest.config.muke.globalconfig.globalConfig import GlobalConfig,gc   #导入全局变量
from WWTest.base.activeBrowser import ActiveBrowser
from WWTest.util.getTimeStr import GetTimeStr
from WWTest.autotest.config.muke.page.indexPage import IndexPage,indexpage   #导入首页
from WWTest.autotest.config.muke.page.avderPage import AvderPage,avderpage,AvderPageFunction,\
    avderpagefunction   #导入广告弹框页
from WWTest.autotest.config.muke.depend.clickAndBackDepend import ClickAndBackDepend,clickandbackdepend
    #导入 ClickAndBack依赖



class TestClickAndBackClass(unittest.TestCase):  # 创建测试类

    @classmethod  # 类方法，只执行一次，但必须要加注解@classmethod,且名字固定为setUpClass
    def setUpClass(cls):
        # cls.activeweb = ActiveBrowser()  # 实例化
        # cls.loginurl = LoginPage().pageurl
        # cls.activeweb.getUrl(indexpage.pageurl)  # 打开网址
        # cls.activeweb.findElementByXpathAndInput(LoginPage().account,AGENT_LOGIN_ACCOUNT)
        # cls.activeweb.findElementByXpathAndInput(LoginPage().password,AGENT_LOGIN_PASSWORD)
        # cls.activeweb.findElementByXpathAndClick(LoginPage().loginbutton)
        # cls.activeweb.delayTime(3)
        # cls.testpage = DetailsPage()
        # cls.testpageurl =cls.testpage.pageurl   #测试页面url
        # cls.activeweb.getUrl(cls.testpageurl)
        # cls.activeweb.delayTime(3)
        pass

    @classmethod  # 类方法，只执行一次，但必须要加注解@classmethod,且名字固定为tearDownClass
    def tearDownClass(cls):
        # cls.activeweb.closeBrowse()
        pass

    def setUp(self):  # 每条用例执行测试之前都要执行此方法
        self.activebrowser = ActiveBrowser()  # 实例化
        self.activebrowser.getUrl(indexpage.pageurl)
        pass

    def tearDown(self):  # 每条用例执行测试之后都要执行此方法
        self.activebrowser.closeBrowse()
        pass


    def definedepend(self,dependid):
        clickandbackdepend.clickandbackdepend(self.activebrowser,dependid)
        # self.activebrowser.outPutMyLog("依赖ID（dependid）为:%s" % dependid)
        # if dependid != None:
        #     self.activebrowser.outPutMyLog("执行依赖")
        #     from testdatas.models import ClickAndBack
        #     clickandbacktestcases = ClickAndBack.objects.filter(id=int(dependid))
        #     print("clickandbacktestcases:%s" % clickandbacktestcases)
        #     if str(clickandbacktestcases) != "<QuerySet []>":
        #         self.activebrowser.outPutMyLog("找到依赖数据")
        #         for clickandbacktestcase in  clickandbacktestcases:
        #             depend = clickandbacktestcase.depend_case_id
        #             self.activebrowser.outPutMyLog("depend:%s" % depend)
        #             if depend != None:
        #                 self.activebrowser.outPutMyLog("进入下一层依赖")
        #                 self.definedepend(depend)
        #
        #             self.activebrowser.outPutMyLog("执行的caseid:%s" % clickandbacktestcase.id)
        #             self.activebrowser.findEleAndClick("%s_%s"%(clickandbacktestcase.id,
        #                                                         clickandbacktestcase.case_counts),
        #                                                clickandbacktestcase.current_page_click_ele_find,
        #                                                clickandbacktestcase.current_page_click_ele_find_value)
        #             is_new = clickandbacktestcase.is_new
        #             if is_new:
        #                 self.activebrowser.switchNewWindows()
        #
        #     else:
        #         self.activebrowser.outPutErrorMyLog("没有找到依赖id[%s]对应的数据！" % dependid)
        # else:
        #     self.activebrowser.outPutMyLog("依赖ID为None，不执行依赖！")



    #定义点击返回函数
    def defineclickandback(self,num,case_counts,depend_case_id,
                           current_page_click_ele_find, current_page_click_ele_find_value,
                           is_new,
                           next_page_check_ele_find,next_page_check_ele_find_value):


        #如果弹出广告弹框，关闭弹框
        if avderpagefunction.isExist_x(self.activebrowser,avderpage.x_xpath):
            self.activebrowser.findElementByXpathAndClick(avderpage.x_xpath)


        #如果有依赖ID，则执行依赖函数，达到执行当前用例的前提条件
        if depend_case_id != None:
            self.definedepend(depend_case_id)
            self.activebrowser.outPutMyLog("依赖函数执行完毕！！！")

        self.activebrowser.outPutMyLog("开始正式执行测试用例")
        #点击当前页面元素
        self.activebrowser.findEleAndClick(num, current_page_click_ele_find, current_page_click_ele_find_value)

        #验证出现预期元素
        #如果出现新窗口,切换到新窗口
        if is_new:
            self.activebrowser.switchNewWindows()
        self.activebrowser.findEleImageNum(num,next_page_check_ele_find,next_page_check_ele_find_value)


    # def test001(self):
    #     print("第一条测试用例")
    #     self.definedepend(self.dependid)

    @staticmethod    #根据不同的参数生成测试用例
    def getTestFunc(num,case_counts,depend_case_id,
                           current_page_click_ele_find, current_page_click_ele_find_value,
                           is_new,
                           next_page_check_ele_find,next_page_check_ele_find_value):

        def func(self):
            self.defineclickandback(num,case_counts,depend_case_id,
                           current_page_click_ele_find, current_page_click_ele_find_value,
                           is_new,
                           next_page_check_ele_find,next_page_check_ele_find_value)
        return func

def __generateTestCases():
    from testdatas.models import ClickAndBack

    clickandbacktestcase_all = ClickAndBack.objects.filter(is_run_case=True).\
        filter(test_project="慕课网 ").order_by('id')

    for clickandbacktestcase in clickandbacktestcase_all:
        forcount = clickandbacktestcase.case_counts
        starttime = GetTimeStr().getTimeStr()
        if len(str(clickandbacktestcase.id)) == 1:
            clickandbacktestcaseid = '0000%s' % clickandbacktestcase.id
        elif len(str(clickandbacktestcase.id)) == 2:
            clickandbacktestcaseid = '000%s' % clickandbacktestcase.id
        elif len(str(clickandbacktestcase.id)) == 3:
            clickandbacktestcaseid = '00%s' % clickandbacktestcase.id
        elif len(str(clickandbacktestcase.id)) == 4:
            clickandbacktestcaseid = '0%s' % clickandbacktestcase.id
        elif len(str(clickandbacktestcase.id)) == 5:
            clickandbacktestcaseid = '%s' % clickandbacktestcase.id
        else:
            clickandbacktestcaseid = 'Id已经超过5位数，请重新定义'

        for i in range(1, forcount + 1):  # 循环，从1开始
            if len(str(i)) == 1:
                forcount_i = '0000%s' % i
            elif len(str(i)) == 2:
                forcount_i = '000%s' % i
            elif len(str(i)) == 3:
                forcount_i = '00%s' % i
            elif len(str(i)) == 4:
                forcount_i = '0%s' % i
            elif len(str(i)) == 5:
                forcount_i = '%s' % i
            else:
                forcount_i = 'Id已经超过5位数，请重新定义'

            args = []
            args.append(clickandbacktestcaseid)
            args.append(i)
            args.append(clickandbacktestcase.depend_case_id)
            args.append(clickandbacktestcase.current_page_click_ele_find)
            args.append(clickandbacktestcase.current_page_click_ele_find_value)
            args.append(clickandbacktestcase.is_new)
            args.append(clickandbacktestcase.next_page_check_ele_find)
            args.append(clickandbacktestcase.next_page_check_ele_find_value)

            setattr(TestClickAndBackClass,
                    'test_func_%s_%s_%s' % (clickandbacktestcaseid, clickandbacktestcase.test_case_title, forcount_i),
                    TestClickAndBackClass.getTestFunc(*args))  # 通过setattr自动为TestCase类添加成员方法，方法以“test_func_”开头


__generateTestCases()

if __name__ == '__main__':
    print("hello world")
    unittest.main()












