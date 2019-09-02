class ClickAndBackDepend(object):
    def clickandbackdepend(self,activebrowser,dependid):
        activebrowser.outPutMyLog("依赖ID（dependid）为:%s" % dependid)
        if dependid != None:
            activebrowser.outPutMyLog("执行依赖")
            from testdatas.models import ClickAndBack
            clickandbacktestcases = ClickAndBack.objects.filter(id=int(dependid))
            print("clickandbacktestcases:%s" % clickandbacktestcases)
            if str(clickandbacktestcases) != "<QuerySet []>":
                activebrowser.outPutMyLog("找到依赖数据")
                for clickandbacktestcase in  clickandbacktestcases:
                    depend = clickandbacktestcase.depend_case_id
                    activebrowser.outPutMyLog("depend:%s" % depend)
                    if depend != None:
                        activebrowser.outPutMyLog("进入下一层依赖")
                        self.clickandbackdepend(activebrowser,depend)

                    activebrowser.outPutMyLog("执行的caseid:%s" % clickandbacktestcase.id)
                    activebrowser.findEleAndClick("%s_%s"%(clickandbacktestcase.id,
                                                                clickandbacktestcase.case_counts),
                                                       clickandbacktestcase.current_page_click_ele_find,
                                                       clickandbacktestcase.current_page_click_ele_find_value)
                    is_new = clickandbacktestcase.is_new
                    if is_new:
                        activebrowser.switchNewWindows()

            else:
                activebrowser.outPutErrorMyLog("没有找到依赖id[%s]对应的数据！" % dependid)
        else:
            activebrowser.outPutMyLog("依赖ID为None，不执行依赖！")

clickandbackdepend = ClickAndBackDepend()