

import xadmin
from xadmin import views   #导入xadmin中的views,用于和 BaseSettings类绑定


class BaseSettings(object):   #全站的配置类, 配置主题
    enable_themes = False  #主题功能,enable_themes=True 表示要使用它的主题功能，xadmin默认是取消掉的
    use_bootswatch = True   #xadmin默认是取消掉的

xadmin.site.register(views.BaseAdminView, BaseSettings)   #注册BaseSettings


class GlobalSettings(object):   ##全站的配置类
    site_title = "自动化测试管理系统"   #页面左上角的标题名称
    site_footer = "测试网"   #页面底部的文字显示内容
    menu_style = "accordion"  # 将一个app下的内容收起来

xadmin.site.register(views.CommAdminView, GlobalSettings)   #注册GlobalSettings





