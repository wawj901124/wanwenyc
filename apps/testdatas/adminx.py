import xadmin

from .models import ClickAndBack,User

class ClickAndBackXAdmin(object):
    all_zi_duan = ["id","test_project","test_module","test_page",
                   "test_case_title","is_run_case",
                   "current_page_click_ele_find","current_page_click_ele_find_value",
                   "is_new",
                   "next_page_check_ele_find","next_page_check_ele_find_value",
                   "case_counts","depend_case","write_user",
                   "add_time","update_time"]
    list_display =  ["test_project","test_module","test_page",
                   "test_case_title","is_run_case",
                   "current_page_click_ele_find","current_page_click_ele_find_value",
                    "is_new",
                   "next_page_check_ele_find","next_page_check_ele_find_value",
                   "case_counts","depend_case",
                     "go_to"]   #定义显示的字段
    list_filter =  ["test_project","test_module","test_page",
                   "test_case_title","is_run_case","is_new",
                    "write_user"] #定义筛选的字段
    search_fields = all_zi_duan   #定义搜索字段
    model_icon = "fa fa-file-text" # 定义图标显示
    ordering = ["-add_time"]  # 添加默认排序规则显示排序，根据添加时间倒序排序
    readonly_fields = ["write_user","add_time","update_time"]  # 设置某些字段为只为可读  #设置了readonly_fields，再设置exclude，exclude对该字段无效，

    # exclude = ['case_step']  # 设置某些字段为不显示，即隐藏  #readonly_fields和exclude设置会有冲突
    # inlines = [TestCaseInline]  # inlines配和TestCaseInline使用，可以直接在项目页面添加测试用例#只能做一层嵌套，不能进行两层嵌套

    list_editable = all_zi_duan   # 可以在列表页对字段进行编辑
    refresh_times = [3, 5]  # 对列表页进行定时刷新,配置了3秒和5秒，可以从中选择一个
    list_per_page = 50   #每页设置50条数据，默认每页展示100条数据
    # fk_fields = ['test_project_id',]  #设置显示外键字段，未生效
    list_display_links = ["test_case_title",]   #设置点击链接进入编辑页面的字段
    # date_hierarchy = 'add_time'   #详细时间分层筛选，未生效
    show_detail_fields = ["test_project",]   #显示数据详情

    list_export = ('xls',)  #控制列表页导出数据的可选格式
    show_bookmarks = True   #控制是否显示书签功能

    #设置是否加入导入插件
    import_excel = True   #True表示显示使用插件，False表示不显示使用插件，该import_excel变量会覆盖插件中的变量

    def save_models(self):   #重载save_models的方法，可以在做了某个动作后，动态重新加载
        obj = self.new_obj   #取得当前用例的实例
        if self.request.user.is_superuser:  # 超级用户则不对编写人做修改
            obj.save()  # 保存当前用例
        else:    #非超级用户会自动保存编写人
            user = User.objects.get(username=self.request.user)
            obj.write_user_id = user.id  #保存当前的write_user为用户登录的user
            obj.save()   #保存当前用例


    def queryset(self):   #重载queryset方法，用来做到不同的admin取出的数据不同
        qs = super(ClickAndBackXAdmin, self).queryset()   #调用父类
        if self.request.user.is_superuser:   #超级用户可查看所有数据
            return qs
        else:
            qs = qs.filter(write_user=self.request.user)  #否则只显示本用户数据
            return qs   #返回qs

xadmin.site.register(ClickAndBack, ClickAndBackXAdmin) #在xadmin中注册ClickAndBackXAdmin



