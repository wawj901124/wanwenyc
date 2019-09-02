
class AvderPage(object):
    #广告弹窗
    x_xpath = "/html/body/div[8]/div/i"

avderpage = AvderPage()

class AvderPageFunction(object):
    def isExist_x(self,activebrowser,x_xpath):
        try:
            activebrowser.driver.find_element_by_xpath(x_xpath)
            return True
        except:
            return False


avderpagefunction = AvderPageFunction()
