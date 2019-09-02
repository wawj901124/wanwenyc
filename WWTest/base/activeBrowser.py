
# ----------------------------------------------------------------------
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wanwenyc.settings")
django.setup()
# ----------------------------------------------------------------------
#独运行某一个py文件时会出现如下错误：django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.，以上内容可以解决此问题,加载django中的App
from wanwenyc.settings import MEDIA_ROOT    #导入Settings中配置的MEDIA_ROOT

#------------------------导入系统包-----------------------------------------
import time   #导入时间
import os
import traceback
import json
import win32gui
import win32con

#------------------------导入第三方包-----------------------------------------
from selenium import webdriver   #导入驱动
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from PIL import Image   #导入Image
from PIL import ImageEnhance  #导入ImageEnhance
import pytesseract   #导入pytesseract
from selenium.webdriver.support.select import Select   #导入Select
from selenium.webdriver.common.action_chains import ActionChains   #导入ActionChains

##------------------------导入自定义的包-----------------------------------------
from WWTest.util.getTimeStr import GetTimeStr   #导入获取时间串函数
from WWTest.util.myLogs import MyLogs



class  ActiveBrowser(object):

    def __init__(self):
        # self.driver = self.getChromeDriver()
        # self.driver = self.getIeDriver()
        self.driver = self.getFirefoxDriver()
        self.timeStr = GetTimeStr()   #实例化


    #使用火狐浏览器
    def getFirefoxDriver(self):
        # binary = FirefoxBinary(r'D:\Program Files (x86)\Mozilla Firefox\firefox.exe')
        # firefoxdriver = webdriver.Firefox(firefox_binary=binary)
        fire_options = webdriver.FirefoxOptions()   #为驱动加入无界面配置
        fire_options.add_argument('--headless')   #为驱动加入无界面配置
        firefoxdriver = webdriver.Firefox()
        # firefoxdriver = webdriver.Firefox(firefox_options=fire_options)  # 需要把驱动所在路径配置到系统环境变量里
        firefoxdriver.maximize_window()   #窗口最大化
        return  firefoxdriver



    #使用谷歌浏览器

    def getChromeDriver(self):
        chrome_options = webdriver.ChromeOptions()   #为驱动加入无界面配置
        chrome_options.add_argument('--headless')   #为驱动加入无界面配置
        # chromedriver = webdriver.Chrome(chrome_options=chrome_options)
        # chromedriver = webdriver.Chrome()  # 需要把驱动所在路径配置到系统环境变量里
        path = r"%s/driver/chromedriver.exe"% str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   #配置驱动路径
        print("path:%s" % path)
        # path = r"D:\Users\Administrator\PycharmProjects\webtestdata\TestCaseFunction\driver\chromedriver.exe"  #配置驱动路径
        option = webdriver.ChromeOptions()
        option.add_argument('--user-data-dir=C:\\Users\\Administrator\\Local\\Google\\Chrome\\User Data\\Default')  # 设置成用户自己的数据目录
                                                                    #浏览器输入chrome://version 下个人资料路径就是自己的数据目录
        chromedriver = webdriver.Chrome(executable_path=path,chrome_options=option)
        chromedriver.maximize_window()   #窗口最大化
        self.delayTime(5)
        return  chromedriver



    #使用IE浏览器
    def getIeDriver(self):
        iedriver = webdriver.Ie()  # 需要把驱动所在路径配置到系统环境变量里
        return  iedriver

    #使用Edge浏览器
    def getEdgeDriver(self):
        edgedriver = webdriver.Edge()  # 需要把驱动所在路径配置到系统环境变量里
        return  edgedriver


    #使用Opera浏览器
    def getOperaDriver(self):
        operadriver = webdriver.Opera  # 需要把驱动所在路径配置到系统环境变量里
        return  operadriver



    def outPutMyLog(self,context):
        mylog = MyLogs(context)
        mylog.runMyLog()


    def outPutErrorMyLog(self,context):
        mylog = MyLogs(context)
        mylog.runErrorLog()



    #打开网址
    def getUrl(self,url):
        try:
            self.driver.get(url)
            self.outPutMyLog("进入网址：%s"% url)
            # print("进入网址：%s"% url)
        except Exception as e:
            self.getScreenshotAboutMySQL()  # 截图关联django服务
            self.outPutErrorMyLog("打开网页失败,关闭驱动.问题描述：[%s]" % e)
            self.closeBrowse()


    #获取当前页面的url
    def getNowPageUrl(self):
        NowPageUrl = self.driver.current_url
        self.outPutMyLog("当前页面的URL为：%s" %  NowPageUrl)
        return NowPageUrl

    #获取元素
    def findELe(self,findstyle,findstylevalue):
        issecond = False
        try:
            if str(findstyle) == "class_name":
                ele = self.driver.find_element_by_class_name(findstylevalue)
                self.outPutMyLog("找到class_name为【%s】的元素" % findstylevalue)
            elif str(findstyle) == "css_selector":
                ele = self.driver.find_element_by_css_selector(findstylevalue)
                self.outPutMyLog("找到css_selector为【%s】的元素" % findstylevalue)
            elif str(findstyle) == "id":
                ele = self.driver.find_element_by_id(findstylevalue)
                self.outPutMyLog("找到id为【%s】的元素" % findstylevalue)
            elif str(findstyle) == "link_text":
                ele = self.driver.find_element_by_link_text(findstylevalue)
                self.outPutMyLog("找到link_text为【%s】的元素" % findstylevalue)
            elif str(findstyle) == "name":
                ele = self.driver.find_element_by_name(findstylevalue)
                self.outPutMyLog("找到name为【%s】的元素" % findstylevalue)
            elif str(findstyle) == "partial_link_text":
                ele = self.driver.find_element_by_partial_link_text(findstylevalue)
                self.outPutMyLog("找到link_text为【%s】的元素" % findstylevalue)
            elif str(findstyle) == "tag_name":
                ele = self.driver.find_element_by_tag_name(findstylevalue)
                self.outPutMyLog("找到tag_name为【%s】的元素" % findstylevalue)
            elif str(findstyle) == "xpath":
                ele = self.driver.find_element_by_xpath(findstylevalue)
                self.outPutMyLog("找到xpath为【%s】的元素" % findstylevalue)
            else:
                self.outPutErrorMyLog("元素的查找方式不再八类（id、name、class_name、tag_name、"
                                      "link_text、partial_link_text、css_selector、xpath）之中，"
                                      "请输入正确的查找方式.")
            self.driver.execute_script("arguments[0].scrollIntoView();", ele)  # 拖动到可见的元素去，影响截取特定区域的截图，不影响整个页面截图
            self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", ele,"background:green;border:2px solid red")   #高亮显示操作的元素
        except Exception as e:
            self.outPutMyLog("问题描述：%s" % e)
            self.getScreenshotNormal()
            self.delayTime(5)
            issecond = True

        if issecond:
            try:
                if str(findstyle) == "class_name":
                    ele = self.driver.find_element_by_class_name(findstylevalue)
                    self.outPutMyLog("再次查找，找到class_name为【%s】的元素" % findstylevalue)
                elif str(findstyle) == "css_selector":
                    ele = self.driver.find_element_by_css_selector(findstylevalue)
                    self.outPutMyLog("再次查找，找到css_selector为【%s】的元素" % findstylevalue)
                elif str(findstyle) == "id":
                    ele = self.driver.find_element_by_id(findstylevalue)
                    self.outPutMyLog("再次查找，找到id为【%s】的元素" % findstylevalue)
                elif str(findstyle) == "link_text":
                    ele = self.driver.find_element_by_link_text(findstylevalue)
                    self.outPutMyLog("再次查找，找到link_text为【%s】的元素" % findstylevalue)
                elif str(findstyle) == "name":
                    ele = self.driver.find_element_by_name(findstylevalue)
                    self.outPutMyLog("再次查找，找到name为【%s】的元素" % findstylevalue)
                elif str(findstyle) == "partial_link_text":
                    ele = self.driver.find_element_by_partial_link_text(findstylevalue)
                    self.outPutMyLog("再次查找，找到link_text为【%s】的元素" % findstylevalue)
                elif str(findstyle) == "tag_name":
                    ele = self.driver.find_element_by_tag_name(findstylevalue)
                    self.outPutMyLog("再次查找，找到tag_name为【%s】的元素" % findstylevalue)
                elif str(findstyle) == "xpath":
                    ele = self.driver.find_element_by_xpath(findstylevalue)
                    self.outPutMyLog("再次查找，找到xpath为【%s】的元素" % findstylevalue)
                else:
                    self.outPutErrorMyLog("元素的查找方式不再八类（id、name、class_name、tag_name、"
                                          "link_text、partial_link_text、css_selector、xpath）之中，"
                                          "请输入正确的查找方式.")
                self.driver.execute_script("arguments[0].scrollIntoView();", ele)  # 拖动到可见的元素去，影响截取特定区域的截图，不影响整个页面截图
                self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", ele,
                                           "background:green;border:2px solid red")  # 高亮显示操作的元素
            except Exception as e:
                self.getScreenshotAboutMySQL()  #截图关联django服务
                # self.getScreenshot()  #截图不关联django服务
                self.outPutErrorMyLog("停顿5秒后再次查找依然未找到元素.问题描述：%s" % e)
                self.closeBrowse()
        return ele

    #获取控件截图
    def findEleImageNum(self,num,findstyle,findstylevalue):
        ele = self.findELe(findstyle,findstylevalue)   #获取元素控件
        pageScreenshotpath = self.getScreenshotNormal()  # 获取整个页面截图
        # location = ele.location   #获取验证码x,y轴坐标   #截取了BUSINESS
        location = ele.location_once_scrolled_into_view  # 获取元素x,y轴坐标   #消除self.driver.execute_script("arguments[0].scrollIntoView();", ele) 对截图的影响 截取了login imgae
        size = ele.size   #获取元素的长宽
        coderange = (int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
        pageScreenshot = Image.open(pageScreenshotpath)   #打开截图
        imageScreen = pageScreenshot.crop(coderange)   #使用Image的crop函数，从截图中再次截取我们需要的区域,即验证码区域
        tStr = self.getTimeStr()
        eleimage = "%s/imagefile/ele/%s_%s_ele.png" % (str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),num,tStr)
        imageScreen.save(eleimage)   #保存控件截图
        self.outPutMyLog('获取到的元素的截图路径为：%s'% eleimage)
        return ele

    #查找元素，然后输入内容
    def findEleAndInputNum(self,num,findstyle,findstylevalue,inputcontent):
        ele = self.findEleImageNum(num,findstyle,findstylevalue)
        ele.clear()   #清除输入框内容
        ele.send_keys(inputcontent)   #输入内容
        # self.delayTime(3)
        displaytext = self.findEleAndReturnValueNum(num,findstyle,findstylevalue,'value')
        if str(inputcontent) == str(displaytext):
            self.outPutMyLog("输入内容：%s;显示内容：%s"% (inputcontent,displaytext))
        else:
            self.outPutErrorMyLog("输入内容：%s;显示内容：%s"% (inputcontent,displaytext))
        # self.delayTime

    #查找元素，然后返回元素的默认显示文字
    def findEleAndReturnValueNum(self,num,findstyle,findstylevalue,valuename):
        ele = self.findEleImageNum(num,findstyle,findstylevalue)
        eletext = ele.get_attribute(valuename)
        self.outPutMyLog("得到的元素属性【%s】的值为：%s"%(valuename,eletext))
        return eletext

    #查找元素，然后点击
    def findEleAndClick(self,num,findstyle,findstylevalue):
        ele = self.findEleImageNum(num,findstyle,findstylevalue)
        ele.click()   #点击
        self.outPutMyLog("点击元素")
        self.delayTime(3)
        return ele




    #通过xpath查找元素
    def findElementByXpath(self,path):
        issecond = False
        try:
            ele = self.driver.find_element_by_xpath(path)
            self.outPutMyLog("找到Xpath为【%s】的元素" % path)
            self.driver.execute_script("arguments[0].scrollIntoView();", ele)  # 拖动到可见的元素去，影响截取特定区域的截图，不影响整个页面截图
            self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", ele,"background:green;border:2px solid red")   #高亮显示操作的元素
            #使用JavaScript代码将传入的页面元素对象的背景颜色和边框颜分别设置为绿色和红色
        except Exception as e:
            self.outPutErrorMyLog("问题描述：%s" % e)
            # print(e)
            self.getScreenshotNormal()
            self.delayTime(5)
            issecond = True

        if issecond:
            try:
                ele = self.driver.find_element_by_xpath(path)
                self.outPutMyLog("再次找到Xpath为【%s】的元素" % path)
                self.driver.execute_script("arguments[0].scrollIntoView();", ele)  # 拖动到可见的元素去，影响截取特定区域的截图，不影响整个页面截图
                self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", ele,"background:green;border:2px solid red")  # 高亮显示操作的元素
                # 使用JavaScript代码将传入的页面元素对象的背景颜色和边框颜分别设置为绿色和红色
                # print("最终找到元素")
            except Exception as e:
                self.getScreenshotAboutMySQL()  #截图关联django服务
                # self.getScreenshot()  #截图不关联django服务
                self.outPutErrorMyLog("停顿5秒后再次查找依然未找到元素.问题描述：%s" % e)
                self.closeBrowse()
                self.isActiveBrowser = True
        return ele



    #获取控件截图
    def getEleImage(self,num,path):
        ele = self.findElementByXpath(path)   #获取元素控件
        pageScreenshotpath = self.getScreenshotNormal()  # 获取整个页面截图
        # location = ele.location   #获取验证码x,y轴坐标   #截取了BUSINESS
        location = ele.location_once_scrolled_into_view  # 获取元素x,y轴坐标   #消除self.driver.execute_script("arguments[0].scrollIntoView();", ele) 对截图的影响 截取了login imgae
        size = ele.size   #获取元素的长宽
        coderange = (int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
        pageScreenshot = Image.open(pageScreenshotpath)   #打开截图
        imageScreen = pageScreenshot.crop(coderange)   #使用Image的crop函数，从截图中再次截取我们需要的区域,即验证码区域
        tStr = self.getTimeStr()
        eleimage = "%s/imagefile/ele/%s_%s_ele.png" % (str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),num,tStr)
        imageScreen.save(eleimage)   #保存控件截图
        self.outPutMyLog('获取到的元素的截图路径为：%s'% eleimage)
        return ele



    #通过xpath查找元素，然后返回元素的text内容
    def findElementByXpathAndReturnText(self,num,path):
        ele = self.getEleImage(num,path)
        eletext = ele.text
        self.outPutMyLog("元素的Xpath路径为：%s;对应的文本信息为：%s"%(path,eletext))
        self.delayTime(3)
        return eletext


    def findElementByXpathAndReturnTextNotNum(self,path):
        ele = self.findElementByXpath(path)
        eletext = ele.text
        self.outPutMyLog("元素的Xpath路径为：%s;对应的文本信息为：%s"%(path,eletext))
        self.delayTime(3)
        return eletext


    #通过xpath查找元素，然后返回元素的标签名(例如input)
    def findElementByXpathAndReturnTagName(self,path):
        ele = self.findElementByXpath(path)
        eletext = ele.tag_name
        return eletext


    #通过xpath查找元素，然后返回元素的默认显示文字
    def findElementByXpathAndReturnValue(self,path,valuename):
        ele = self.findElementByXpath(path)
        eletext = ele.get_attribute(valuename)
        return eletext



    #通过xpath查找元素，然后返回元素的默认显示文字
    def findElementByXpathAndReturnValueNum(self,num,path,valuename):
        ele = self.getEleImage(num,path)
        eletext = ele.get_attribute(valuename)
        self.outPutMyLog("得到的元素属性【%s】的值为：%s"%(valuename,eletext))
        return eletext



    #通过xpath查找元素，然后输入内容
    def findElementByXpathAndInput(self,path,inputcontent):
        ele = self.findElementByXpath(path)
        ele.clear()   #清除输入框内容
        ele.send_keys(inputcontent)   #输入内容



    #通过xpath查找元素，然后输入内容
    def findElementByXpathAndInputNum(self,num,path,inputcontent):
        ele = self.getEleImage(num, path)
        ele.clear()   #清除输入框内容
        ele.send_keys(inputcontent)   #输入内容
        # self.delayTime(3)
        displaytext = self.findElementByXpathAndReturnValueNum(num,path,'value')
        self.outPutMyLog("输入内容：%s;显示内容：%s"% (inputcontent,displaytext))
        # self.delayTime



    #通过xpath查找元素，然后情况输入框中的内容
    def findElementByXpathAndDeleteInputContentNum(self,num,path):
        ele = self.getEleImage(num, path)
        displaytext = self.findElementByXpathAndReturnValueNum(num,path,'value')
        ele.clear()   #清除输入框内容
        self.outPutMyLog("已经删除内容：%s."% displaytext)
        # self.delayTime(3000)


    #通过xpath查找元素，移除其Readonly属性然后输入内容

    def findElementByXpathAndInputNumRemoveReadonly(self,num,path,inputcontent):
        ele = self.getEleImage(num, path)
        #移除Readonly属型
        self.removeReadonly(ele)
        ele.clear()   #清除输入框内容
        ele.send_keys(inputcontent)   #输入内容
        # 设置Readonly属型为空
        self.setReadonly(ele)
        # 点击使日期谈框消失
        self.mockClickBlank(0,0)
        displaytext = self.findElementByXpathAndReturnValueNum(num,path,'value')
        self.outPutMyLog("输入内容：%s;显示内容：%s"% (inputcontent,displaytext))
        # self.delayTime(3000)



    #通过xpath查找元素，使用JS直接设置Input框属性值（value=）
    def findElementByXpathAndInputNumJsSetValue(self,num,path,inputcontent):
        ele = self.getEleImage(num, path)
        self.jsSetValue(ele,inputcontent)
        displaytext = self.findElementByXpathAndReturnValueNum(num,path,'value')
        self.outPutMyLog("输入内容：%s;显示内容：%s"% (inputcontent,displaytext))
        # self.delayTime(3000)



    # 通过xpath查找元素，然后点击日期input框，点击选择日期路径

    #日期控件路径path1，日期路径path2，日期左移月路径path3,日期右移月路径path4
    def findElementByXpathAndClickAbountData(self, num, path1,path2,pathleft=None,pathright=None,pathconfirm=None):
        #点击日期input框
        self.findElementByXpathAndClickNum(num,path1)
        if pathleft != None:
            #点击日期左移月按钮
            self.findElementByXpathAndClickNum(num, pathleft)
        if pathright != None:
            #点击日期右移月按钮
            self.findElementByXpathAndClickNum(num, pathright)
        #点击日期日路径
        self.findElementByXpathAndClickNum(num,path2)
        if pathconfirm !=None:
            self.findElementByXpathAndClickNum(num, pathconfirm)
        displaytext = self.findElementByXpathAndReturnValueNum(num, path1, 'value')
        self.outPutMyLog("日期显示内容：%s" % displaytext)
        self.mockClickBlank(0,0)



    # 通过xpath查找元素，然后点击日期input框，点击选择日期路径,选择时分秒（预留）
    #日期控件路径path1，日期路径path2，分路径path3，日期左移月路径pathleft,日期右移月路径pathright
    def findElementByXpathAndClickAbountDataToSecound(self, num, path1,path2,path3,pathleft=None,pathright=None):
        #点击日期input框
        self.findElementByXpathAndClickNum(num,path1)
        if pathleft != None:
            #点击日期左移月按钮
            self.findElementByXpathAndClickNum(num, pathleft)
        if pathright != None:
            #点击日期右移月按钮
            self.findElementByXpathAndClickNum(num, pathright)
        #点击日期日路径
        self.findElementByXpathAndClickNum(num,path2)
        #点击日期时分秒路径
        self.findElementByXpathAndClickNum(num,path3)
        displaytext = self.findElementByXpathAndReturnValueNum(num, path1, 'value')
        self.outPutMyLog("日期显示内容：%s" % displaytext)
        self.mockClickBlank(0,0)


    #通过xpath查找元素，设置其Readonly属性值为空
    def findElementByXpathAndInputNumSetReadonly(self,num,path):
        ele = self.getEleImage(num, path)
        self.setReadonly(ele)
        # self.delayTime(3000)


    #通过xpath查找元素，然后点击
    def findElementByXpathAndClick(self,path):
        ele = self.findElementByXpath(path)
        ele.click()   #点击
        self.outPutMyLog("点击元素的Xpath路径为：%s" % path)
        # print("点击元素的Xpath路径为：%s" % path)
        self.delayTime(3)
        return ele


    #通过xpath查找元素，然后点击
    def findElementByXpathAndClickNum(self,num,path):
        self.delayTime(1)
        ele = self.getEleImage(num,path)
        ele.click()   #点击
        self.outPutMyLog("点击Xpath路径为[%s]的元素" % path)
        # print("点击元素的Xpath路径为：%s" % path)
        self.delayTime(2)
        return ele


    #通过xpath查找元素，然后点击
    def findElementByXpathAndScriptClick(self,path):
        ele = self.findElementByXpath(path)
        self.driver.execute_script("arguments[0].click();", ele)
        self.delayTime(3)
        return ele


    #通过xpath查找元素，然后点击
    def findElementByXpathAndScriptClickNum(self,num,path):
        self.delayTime(1)
        ele = self.getEleImage(num,path)
        self.driver.execute_script("arguments[0].click();", ele)
        self.outPutMyLog("点击xpath为[%s]的元素" % path )
        self.delayTime(2)
        return ele


    #通过xpath查找到要输入文件的input元素，然后上传文件
    def findElementByXpathAndAndFile(self,path,filepath):
        ele = self.findElementByXpath(path)
        try:
            ele.send_keys(filepath)
            self.delayTime(1)
        except Exception as e:
            self.outPutErrorMyLog("上传文件失败，关闭驱动.问题描述：%s"% e)
            self.closeBrowse()



    #通过xpath查找到要输入文件的input元素，然后上传文件
    def findElementByXpathAndAndFileNum(self,num,path,filepath):
        ele = self.getEleImage(num,path)
        try:
            ele.send_keys(filepath)
            self.delayTime(1000)
        except Exception as e:
            self.outPutErrorMyLog("上传文件失败，关闭驱动.问题描述：%s"% e)
            self.closeBrowse()



    #通过xpath查找到要输入文件的input元素，然后上传文件
    #pip install SendKeys
    #import win32gui
    #import win32con
    #import time
    def findElementByXpathAndAndFileNumVue(self,num,path,filepath):
        ele = self.findElementByXpathAndScriptClickNum(num,path)
        # ele = self.getEleImage(num,path)
        try:
            #pip install pywin32
            #import win32gui
            # import win32con
            #文件名：D:\pic\1.jpg
            dialog = win32gui.FindWindow('#32770', '文件上传')  # 对话框
            ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
            ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
            Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
            button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button
            win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, filepath)  # 往输入框输入绝对地址
            win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button
            self.delayTime(5)
        except Exception as e:
            self.outPutErrorMyLog("上传文件失败，关闭驱动.问题描述：%s"% e)
            # self.delayTime(1000)
            self.closeBrowse()



    #通过xpath查找到select元素,然后点击，然后点击要选择的项
    def findElementByXpathAndClickOptionXpath(self,xpath,optiontextxpath):
        try:
            self.findElementByXpathAndScriptClick(xpath)
            self.findElementByXpathAndScriptClick(optiontextxpath)
            self.delayTime(2)
        except Exception as e:
            self.outPutErrorMyLog("出现问题，关闭驱动.问题描述：%s" % e)
            self.closeBrowse()



    #通过xpath查找到select元素,然后点击，然后点击要选择的项
    def findElementByXpathAndClickOptionXpathNum(self,num,xpath,optiontextxpath):
        try:
            self.findElementByXpathAndScriptClickNum(num,xpath)
            self.findElementByXpathAndScriptClickNum(num,optiontextxpath)
            self.delayTime(2)
        except Exception as e:
            self.outPutErrorMyLog("出现问题，关闭驱动.问题描述：%s"% e)
            self.closeBrowse()

    #通过xpath查找到select元素,选择要选择的项
    def findElementByXpathAndReturnOptions(self,path,optiontext):
        ele = Select(self.findElementByXpath(path))
        try:
            selectoption = ele.select_by_visible_text(optiontext)
            self.delayTime(2)
        except Exception as e:
            self.outPutMyLog("填写内容与选项内容对不上，关闭驱动.问题描述：%s"% e)
            self.closeBrowse()

    #通过xpath查找到select元素,选择要选择的项
    def findElementByXpathAndReturnOptionsNum(self,num,path,optiontext):
        ele = Select(self.getEleImage(num,path))
        try:
            selectoption = ele.select_by_visible_text(optiontext)
            self.delayTime(2)
        except Exception as e:
            self.outPutErrorMyLog("填写内容与选项内容对不上，关闭驱动.问题描述：%s"% e)
            self.closeBrowse()

    #通过xpath查找到select并打印其所有的options
    def findElementByXpathAndReturnAllOptions(self,path):
        ele = Select(self.findElementByXpath(path))
        optionlist = []
        try:
            all_options = ele.options
            # print('所有选项内容如下：',all_options)
            for option in all_options:
                optionlist.append(option.text)
                # print('选项内容为：',option.text)
            self.outPutMyLog('获取的选项所有内容：%s'% optionlist)
            return optionlist
        except Exception as e:
            self.outPutErrorMyLog("获取选项内容出错，关闭驱动.问题描述%e"% e)
            self.closeBrowse()



    #通过xpath查找到tbody并打印表格里所有内容
    def findElementByXpathAndReturnTable(self,path):
        ele = self.findElementByXpath(path)
        # print('tagname:',ele.tag_name)
        tabledic = {}
        try:
            trlist = ele.find_elements_by_tag_name('tr')
            # print(len(trlist))
            for i in range(0,len(trlist)):
                # print('第%s行内容如下:\n'% str(i+1))
                #遍历行对象，并获取每一行中所有列对象
                tdlist = trlist[i].find_elements_by_tag_name('td')
                collist = []
                for j in range(0,len(tdlist)):
                    #遍历表格中的列，并打印单元格内容
                    collist.append(tdlist[j].text)
                    # print('第%s列内容如下：'% str(j+1),tdlist[j].text)
                    tabledic[i+1] = collist
            self.outPutMyLog('获取的表格内容：%s'% tabledic)
            # print('获取的表格内容：',tabledic)
            return tabledic
            # print('列表内容为：',option.text)
        except Exception as e:
            self.outPutErrorMyLog("获取表格内容出错，关闭驱动.问题描述：%s"% e)
            self.closeBrowse()



    #通过xpath查找到tbody并打印表格里所有内容
    def findElementByXpathAndReturnTableNum(self,num,path):
        ele = self.getEleImage(num,path)
        # ele = self.findElementByXpath(path)
        # print('tagname:',ele.tag_name)
        tabledic = {}
        try:
            trlist = ele.find_elements_by_tag_name('tr')
            # print(len(trlist))
            for i in range(0,len(trlist)):
                # print('第%s行内容如下:\n'% str(i+1))
                #遍历行对象，并获取每一行中所有列对象
                tdlist = trlist[i].find_elements_by_tag_name('td')
                collist = []
                for j in range(0,len(tdlist)):
                    #遍历表格中的列，并打印单元格内容
                    collist.append(tdlist[j].text)
                    # print('第%s列内容如下：'% str(j+1),tdlist[j].text)
                    tabledic[i+1] = collist
            self.outPutMyLog('获取的表格内容：%s'%tabledic)
            # print('获取的表格内容：',tabledic)
            return tabledic
            # print('列表内容为：',option.text)
        except Exception as e:
            self.outPutErrorMyLog("获取表格内容出错，关闭驱动.问题描述：%s"% e)
            self.closeBrowse()



    def checktable(self,path,inputtext,colnum):

        tabledic = self.findElementByXpathAndReturnTable(path)

        for value in tabledic.values():

            if inputtext.lower() in value[colnum].lower():

                self.outPutMyLog('input输入内容变小写：%s'% inputtext.lower())

                self.outPutMyLog('搜索到的表格内容变小写：%s'% value[colnum].lower())
            else:
                self.outPutMyLog("搜索到的内容不匹配！！！")




    #获取页面截图
    def getScreenshot(self):
        driver = self.driver
        self.outPutMyLog("调用截取图片函数")
        tStr = self.getTimeStr()   #获取当前时间串
        currentny = self.getTimeStrNY()   #获取当前时间的年月

        # path = "../imagefile/%s.png"% tStr

        # path = '%s/screenshots/screenpicture_%s.png' % (

        # str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), tStr)

        firedir = r'%s/media/report/%s/screenshots/' % (os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),currentny)
        self.createdir(firedir)
        path = '%s/screenpicture_%s.png' % (firedir,tStr)
        print(path)
        driver.get_screenshot_as_file(path)
        self.outPutMyLog("*****")
        self.outPutMyLog(path)
        self.outPutMyLog("*****")
        return path



    #获取页面截图
    def getScreenshotAboutMySQL(self):
        driver = self.driver
        self.outPutErrorMyLog("调用截取图片函数")
        tStr = self.getTimeStr()   #获取当前时间串
        currentny = self.getTimeStrNY()   #获取当前时间的年月
        firedir = r'%s/media/report/%s/screenshots/' % (os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),currentny)
        self.createdir(firedir)
        path = '%s/screenpicture_%s.png' % (firedir,tStr)
        pathaboutmysql = r'media\report\%s\screenshots\screenpicture_%s.png'%(currentny,tStr)
        driver.get_screenshot_as_file(path)
        self.outPutErrorMyLog("*****")
        self.outPutErrorMyLog(pathaboutmysql)  #打印截图路径，供报告截图使用
        self.outPutErrorMyLog("*****")
        return path



    #获取页面截图
    def getScreenshotNormal(self):
        driver = self.driver
        self.outPutMyLog("调用截取图片函数")
        tStr = self.getTimeStr()
        path = "%s/imagefile/%s.png"% (str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),tStr)
        driver.get_screenshot_as_file(path)
        return path



    #获取code码截图
    def getCodeImage(self,path):
        pageScreenshotpath = self.getScreenshotNormal()  # 获取整个页面截图
        image = self.findElementByXpath(path)   #获取图片验证码控件
        # location = image.location   #获取验证码x,y轴坐标
        location = image.location_once_scrolled_into_view  # 获取验证码x,y轴坐标   #消除self.driver.execute_script("arguments[0].scrollIntoView();", ele) 对截图的影响
        size = image.size   #获取验证码的长宽
        coderange = (int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
        pageScreenshot = Image.open(pageScreenshotpath)   #打开截图
        imageScreen = pageScreenshot.crop(coderange)   #使用Image的crop函数，从截图中再次截取我们需要的区域,即验证码区域
        tStr = self.getTimeStr()
        path = "%s/imagefile/%s_code.png"%(str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),tStr)
        imageScreen.save(path)   #保存验证码图片
        return tStr


    #获取验证码文字信息
    def getcodetext(self,path):
        imagecodestr = self.getCodeImage(path)
        imagecode = Image.open("%s/imagefile/%s_code.png" % (str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),imagecodestr)) # 打开验证码图片
        pixtongji = []
        for x in range(imagecode.size[1]):
            for y in range(imagecode.size[0]):
                # 遍历图片的xy坐标像素点颜色
                pix = imagecode.getpixel((y, x))
                pixtongji.append(pix)
        nonepixtongjidic = {}
        for item in pixtongji:
            if item in nonepixtongjidic.keys():
                nonepixtongjidic[item] += 1
            else:
                nonepixtongjidic[item] = 1
        self.outPutMyLog("nonepixtongjidic:%s" % nonepixtongjidic)
        nonepixtongjilist = sorted(nonepixtongjidic.values(),reverse=True)   #按照键值对的值对字典进行倒序排序
        numvalue = []
        numvalue.append(nonepixtongjilist[1])   #获取第二个值
        getkey = self.getDictKey(nonepixtongjidic,numvalue)
        img_new = Image.new('P', imagecode.size, 255)
        for x in range(imagecode.size[1]):
            for y in range(imagecode.size[0]):
                # 遍历图片的xy坐标像素点颜色
                pix = imagecode.getpixel((y, x))
                # print(pix)
                # 自己调色，r（pix[0]）=0，g（pix[1]）=0，b（pix[2]）>0为蓝色
                for i in range(len(getkey)):
                    if (pix[0] == getkey[i][0] and pix[1] == getkey[i][1] and pix[2] == getkey[i][2]):
                        # 把遍历的结果放到新图片上，0为透明度，不透明
                        img_new.putpixel((y, x), 0)
        newpath = "%s/imagefile/%s_codegary.png" % (str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),imagecodestr)
        img_new.save(newpath, format='png')
        imagecode = Image.open(newpath)   #打开验证码图片
        imgry = imagecode.convert('L')  # 图像加强，二值化，PIL中有九种不同模式。分别为1，L，P，RGB，RGBA，CMYK，YCbCr，I，F。L为灰度图像
        sharpness = ImageEnhance.Contrast(imgry)   #对比度增强
        imagecodegary = sharpness.enhance(2.0)#2.0为图像的饱和度
        imagecodegary.save(newpath)   #保存灰度值验证码
        endcode = Image.open(newpath)    #打开灰度值验证码
        codetext = pytesseract.image_to_string(endcode).strip()   #获取验证码文本文件
        return codetext



    #获取字典对应值的键
    def getDictKey(self,dict,prevalue):
        getkey = []
        for key,value in dict.items():
            for i in range(len(prevalue)):
                if value == prevalue[i]:
                    getkey.append(key)
        return getkey


    #获取时间串
    def getTimeStr(self):
        tStr = self.timeStr.getTimeStr()
        return tStr

    def getTimeStrNY(self):
        tStrNY = self.timeStr.getTimeStrNY()
        return tStrNY


    #获取cookies
    def getCookies(self):
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            self.outPutMyLog("获取的cookie的值为：%s" % cookie)
        return cookies



    #写入cookies
    def writerCookies(self,cookies,url,url2):
        self.outPutMyLog("\n开始写入cookie-----------------\n")
        self.getUrl(url)
        long = len(cookies)
        for i in range(long):
            cookie = {'name': cookies[i]['name'], 'value': cookies[i]['value']}
            self.driver.add_cookie(cookie)   #selenium添加cookies时，得先登录网址才能添加cookies的
            self.outPutMyLog("写入cookie的值为：%s" % cookie)
        self.driver.refresh()  #
        self.outPutMyLog("刷新当前页面---------")
        self.getUrl(url2)
        self.outPutMyLog("url2为：%s."% url2)
        self.driver.refresh()   #刷新当前页面
        self.outPutMyLog("刷新当前页面---------")
        self.delayTime(5000)   #等待10秒
        self.getCookies()


    #延迟3秒
    def delayTime(self,dalaytime):
        time.sleep(int(dalaytime))   #延迟，
        self.outPutMyLog("等待%s秒---"% dalaytime)


    #使用js去掉input框中的readonly（只读）属性，设置为可输入状态，主要处理日期输入
    def removeReadonly(self,ele):
        self.driver.execute_script("arguments[0].removeAttribute('readonly')", ele)  # 使用js去掉元素中的readonly属性
        self.outPutMyLog("移除input元素中readonly属性，使其可编辑")


    def setReadonly(self,ele):
        self.driver.execute_script("arguments[0].setAttribute('readOnly','')", ele)  # 使用js去掉元素中的readonly属性
        self.outPutMyLog("设置input元素中readonly属性值为true，使其不可编辑")


    #用js方法输入日期
    def jsSetValue(self,ele,value):
        self.driver.execute_script("arguments[0].value='%s'" % value, ele)  # 使用js去掉元素中的readonly属性
        self.outPutMyLog("设置input元素中value属性值为%s" % value)
        self.delayTime(1)



    #模拟鼠标点击空白处
    def mockClickBlank(self,xoffset, yoffset):
        action = ActionChains(self.driver)
        action.move_by_offset(xoffset, yoffset).click().perform()  #点击空白区域：坐标（0，0）
        self.outPutMyLog("模拟点击空白区域（点击坐标（%s，%s））" % (xoffset, yoffset))
        self.delayTime(1)


    def createdir(self,filedir):
        filelist = filedir.split("/")
        # print(filelist)
        long = len(filelist)
        # print(long)
        zuhefiledir = filelist[0]
        for i in range(1,long):
            zuhefiledir = zuhefiledir+"/"+filelist[i]
            if os.path.exists(zuhefiledir):
                self.outPutMyLog("已经存在目录：%s" % zuhefiledir)
            else:
                os.mkdir(zuhefiledir)
                self.outPutMyLog("已经创建目录：%s" % zuhefiledir)

    def clickBack(self):
        self.driver.back()
        url = self.getNowPageUrl()
        self.outPutMyLog("返回到页面URL为：%s的页面" % url)

    def switchNewWindows(self):
        window_handles = self.driver.window_handles
        long = len(window_handles)
        self.outPutMyLog("目前打开的窗口有%s个。" % long)
        window_before = self.driver.window_handles[long-2]
        print("之前窗口的窗口句柄作为:%s" % window_before)
        window_after = self.driver.window_handles[long-1]
        print("新打开的窗口的窗口句柄作为:%s"% window_after)
        self.driver.switch_to.window(window_after)
        # print("当前窗口：%s" % self.driver.current_window_handle)
        #
        # handles = self.driver.window_handles  # 输出当前所有句柄
        # print("所有窗口：%s" % handles)
        # for handle in handles:
        #     if handle != self.driver.current_window_handle:
        #         print("目前条件：%s" % handle)
        #         self.driver.switch_to.window(handle)
        self.delayTime(3)
        print("切换到新窗口")


    #关闭浏览器
    def closeBrowse(self):
        self.driver.quit()


if __name__ == "__main__":
    #驱动下载地址：https://www.cnblogs.com/yhleng/p/8056120.html

    activeweb = ActiveBrowser() #实例化
    url = "https://www.imooc.com/user/newlogin"
    activeweb.getUrl(url)
    account = "/html/body/div[2]/div/div/div[2]/div/form/div[1]/input"
    password = "/html/body/div[2]/div/div/div[2]/div/form/div[2]/input"
    loginbutton = "/html/body/div[2]/div/div/div[2]/div/form/div[5]/input"
    activeweb.findElementByXpathAndInput(account, '17090177294')
    activeweb.findElementByXpathAndInput(password, '900805')
    activeweb.findElementByXpathAndClick(loginbutton)
    activeweb.delayTime(3)
