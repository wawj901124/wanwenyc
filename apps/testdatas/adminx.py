import xadmin

from .models import ClickAndBack,User,NewAddAndCheck
from .models import InputTapInputText,SelectTapSelectOption

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

    def post(self,request, *args,**kwargs):   #重载post函数，用于判断导入的逻辑
        if 'excel' in request.FILES:  #如果excel在request.FILES中
            excel_file = request.FILES.get('excel', '')

            import xlrd   #导入xlrd
            #常用的Excel文件有.xls和.xls两种，.xls文件读取时需要设置formatting_info = True
            # data = xlrd.open_workbook(filename=None, file_contents=excel_file.read())  # xlsx文件

            exceldata = xlrd.open_workbook(filename=None, file_contents=excel_file.read(), formatting_info=True)  # xls文件

            from .analyzexls import Analyzexls
            analyzexls = Analyzexls()
            #将获取的数据循环导入数据库中
            all_list_1 = analyzexls.get_sheets_mg(exceldata, 0)
            i = 0
            if len(all_list_1[0]) == 13:
                while i < len(all_list_1):
                    clickandback = ClickAndBack()  # 数据库的对象等于ClickAndBack,实例化
                    clickandback.test_project = all_list_1[i][0]  # 填写项目all_list_1[i][j]
                    clickandback.test_module = all_list_1[i][1]  # 填写模块
                    clickandback.test_page = all_list_1[i][2]  # 填写测试页
                    clickandback.test_case_title = all_list_1[i][3]  # 填写测试内容的名称
                    if all_list_1[i][4] == "TRUE":
                        clickandback.is_run_case = 1 # 填写是否运行
                    elif all_list_1[i][4] == "FALSE":
                        clickandback.is_run_case = 0  # 填写是否运行

                    clickandback.current_page_click_ele_find = all_list_1[i][5]  # 填写当前页面要点击元素查找风格
                    clickandback.current_page_click_ele_find_value = all_list_1[i][6]  # 填写当前页面要点击元素查找风格的确切值
                    if all_list_1[i][7] == "TRUE":
                        clickandback.is_new = 1  # 填写是否新窗口
                    elif all_list_1[i][7] == "FALSE":
                        clickandback.is_new = 0  # 填写是否新窗口
                    clickandback.next_page_check_ele_find = all_list_1[i][8]  # 填写next_page_check_ele_find
                    clickandback.next_page_check_ele_find_value = all_list_1[i][9]  # 填写next_page_check_ele_find_value
                    clickandback.case_counts = all_list_1[i][10] # 填写case_counts

                    if all_list_1[i][11] != None:  #如果依赖列有内容且内容存在数据库中，则保存依赖内容
                        depend = all_list_1[i][11]
                        depend_contents = ClickAndBack.objects.filter(test_case_title=depend)
                        depend_count = depend_contents.count()
                        if depend_count == 1:
                            for depend_content in depend_contents:
                                clickandback.depend_case_id = depend_content.id

                    if all_list_1[i][12] != None:  # 如果编写人列有数据则填写编写人
                        users = User.objects.all()
                        for user in users:
                            if user.username == all_list_1[i][12]:
                                clickandback.write_user_id = user.id   # 填写编写人
                    clickandback.save()  # 保存到数据库

                    i = i+1
            pass
        return super(ClickAndBackXAdmin,self).post(request,args,kwargs)   #必须调用clickandbackAdmin父类，再调用post方法，否则会报错
                                                                      #一定不要忘记，否则整个ClickAndBackXAdmin保存都会出错


class NewAddAndCheckXadmin(object):
    all_zi_duan = ["id", "test_project", "test_module", "test_page",
                   "test_case_title", "is_run_case",
                   "depend_click_case","confirm_ele_find",
                   "confirm_ele_find_value",
                   "is_click_cancel",
                   "cancel_ele_find","cancel_ele_find_value",
                   "case_counts",  "write_user",
                   "add_time", "update_time"]
    list_display = ["test_project", "test_module", "test_page",
                    "test_case_title", "is_run_case",
                    "depend_click_case", "confirm_ele_find",
                    "confirm_ele_find_value",
                    "is_click_cancel",
                    "cancel_ele_find", "cancel_ele_find_value",
                    "case_counts",]  # 定义显示的字段
    list_filter = ["test_project", "test_module", "test_page",
                   "test_case_title", "is_run_case",
                   "write_user"]  # 定义筛选的字段
    search_fields = all_zi_duan  # 定义搜索字段
    model_icon = "fa fa-file-text"  # 定义图标显示
    ordering = ["-add_time"]  # 添加默认排序规则显示排序，根据添加时间倒序排序
    readonly_fields = ["write_user", "add_time",
                       "update_time"]  # 设置某些字段为只为可读  #设置了readonly_fields，再设置exclude，exclude对该字段无效，

    # exclude = ['case_step']  # 设置某些字段为不显示，即隐藏  #readonly_fields和exclude设置会有冲突
    # inlines = [TestCaseInline]  # inlines配和TestCaseInline使用，可以直接在项目页面添加测试用例#只能做一层嵌套，不能进行两层嵌套

    list_editable = all_zi_duan  # 可以在列表页对字段进行编辑
    refresh_times = [3, 5]  # 对列表页进行定时刷新,配置了3秒和5秒，可以从中选择一个
    list_per_page = 50  # 每页设置50条数据，默认每页展示100条数据
    # fk_fields = ['test_project_id',]  #设置显示外键字段，未生效
    list_display_links = ["test_case_title", ]  # 设置点击链接进入编辑页面的字段
    # date_hierarchy = 'add_time'   #详细时间分层筛选，未生效
    show_detail_fields = ["test_project", ]  # 显示数据详情

    list_export = ('xls',)  # 控制列表页导出数据的可选格式
    show_bookmarks = True  # 控制是否显示书签功能

    # 设置是否加入导入插件
    import_excel = True  # True表示显示使用插件，False表示不显示使用插件，该import_excel变量会覆盖插件中的变量

    #设置内联
    class InputTapInputTextInline(object):
        model = InputTapInputText
        exclude = ["add_time","update_time"]
        extra = 1
        style = 'tab'    #以标签形式展示

    #设置内联
    class SelectTapSelectOptionInline(object):
        model = SelectTapSelectOption
        exclude = ["add_time","update_time"]
        extra = 1
        style = 'tab'    #以标签形式展示

    inlines = [InputTapInputTextInline,SelectTapSelectOptionInline]

    def save_models(self):  # 重载save_models的方法，可以在做了某个动作后，动态重新加载
        obj = self.new_obj  # 取得当前用例的实例
        if self.request.user.is_superuser:  # 超级用户则不对编写人做修改
            obj.save()  # 保存当前用例
        else:  # 非超级用户会自动保存编写人
            user = User.objects.get(username=self.request.user)
            obj.write_user_id = user.id  # 保存当前的write_user为用户登录的user
            obj.save()  # 保存当前用例

    def queryset(self):  # 重载queryset方法，用来做到不同的admin取出的数据不同
        qs = super(NewAddAndCheckXadmin, self).queryset()  # 调用父类
        if self.request.user.is_superuser:  # 超级用户可查看所有数据
            return qs
        else:
            qs = qs.filter(write_user=self.request.user)  # 否则只显示本用户数据
            return qs  # 返回qs

    # def post(self, request, *args, **kwargs):  # 重载post函数，用于判断导入的逻辑
    #     if 'excel' in request.FILES:  # 如果excel在request.FILES中
    #         excel_file = request.FILES.get('excel', '')
    #
    #         import xlrd  # 导入xlrd
    #         # 常用的Excel文件有.xls和.xls两种，.xls文件读取时需要设置formatting_info = True
    #         # data = xlrd.open_workbook(filename=None, file_contents=excel_file.read())  # xlsx文件
    #
    #         exceldata = xlrd.open_workbook(filename=None, file_contents=excel_file.read(),
    #                                        formatting_info=True)  # xls文件
    #
    #         from .analyzexls import Analyzexls
    #         analyzexls = Analyzexls()
    #         # 将获取的数据循环导入数据库中
    #         all_list_1 = analyzexls.get_sheets_mg(exceldata, 0)
    #         i = 0
    #         if len(all_list_1[0]) == 13:
    #             while i < len(all_list_1):
    #                 clickandback = ClickAndBack()  # 数据库的对象等于ClickAndBack,实例化
    #                 clickandback.test_project = all_list_1[i][0]  # 填写项目all_list_1[i][j]
    #                 clickandback.test_module = all_list_1[i][1]  # 填写模块
    #                 clickandback.test_page = all_list_1[i][2]  # 填写测试页
    #                 clickandback.test_case_title = all_list_1[i][3]  # 填写测试内容的名称
    #                 if all_list_1[i][4] == "TRUE":
    #                     clickandback.is_run_case = 1  # 填写是否运行
    #                 elif all_list_1[i][4] == "FALSE":
    #                     clickandback.is_run_case = 0  # 填写是否运行
    #
    #                 clickandback.current_page_click_ele_find = all_list_1[i][5]  # 填写当前页面要点击元素查找风格
    #                 clickandback.current_page_click_ele_find_value = all_list_1[i][6]  # 填写当前页面要点击元素查找风格的确切值
    #                 if all_list_1[i][7] == "TRUE":
    #                     clickandback.is_new = 1  # 填写是否新窗口
    #                 elif all_list_1[i][7] == "FALSE":
    #                     clickandback.is_new = 0  # 填写是否新窗口
    #                 clickandback.next_page_check_ele_find = all_list_1[i][8]  # 填写next_page_check_ele_find
    #                 clickandback.next_page_check_ele_find_value = all_list_1[i][9]  # 填写next_page_check_ele_find_value
    #                 clickandback.case_counts = all_list_1[i][10]  # 填写case_counts
    #
    #                 if all_list_1[i][11] != None:  # 如果依赖列有内容且内容存在数据库中，则保存依赖内容
    #                     depend = all_list_1[i][11]
    #                     depend_contents = ClickAndBack.objects.filter(test_case_title=depend)
    #                     depend_count = depend_contents.count()
    #                     if depend_count == 1:
    #                         for depend_content in depend_contents:
    #                             clickandback.depend_case_id = depend_content.id
    #
    #                 if all_list_1[i][12] != None:  # 如果编写人列有数据则填写编写人
    #                     users = User.objects.all()
    #                     for user in users:
    #                         if user.username == all_list_1[i][12]:
    #                             clickandback.write_user_id = user.id  # 填写编写人
    #                 clickandback.save()  # 保存到数据库
    #
    #                 i = i + 1
    #         pass
    #     return super(ClickAndBackXAdmin, self).post(request, args, kwargs)  # 必须调用clickandbackAdmin父类，再调用post方法，否则会报错
    #     # 一定不要忘记，否则整个ClickAndBackXAdmin保存都会出错


xadmin.site.register(ClickAndBack, ClickAndBackXAdmin) #在xadmin中注册ClickAndBackXAdmin
xadmin.site.register(NewAddAndCheck,NewAddAndCheckXadmin)  #在xadmin中注册NewAddAndCheckXadmin



