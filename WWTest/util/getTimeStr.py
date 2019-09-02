import datetime
import os

from WWTest.util.myLogs import MyLogs


class GetTimeStr:

    def getTimeStr(self):
        now_time = datetime.datetime.now()
        timestr = now_time.strftime('%Y%m%d%H%M%S')
        self.outPutMyLog("当前时间：%s"% now_time)
        self.outPutMyLog("时间串：%s"% timestr)
        return timestr

    def getTimeStrNY(self):
        now_time = datetime.datetime.now()
        timestr = now_time.strftime('%Y%m')
        self.outPutMyLog("当前时间：%s"% now_time)
        self.outPutMyLog("时间串年月：%s"% timestr)
        return timestr

    def outPutMyLog(self,context):
        mylog = MyLogs(context)
        mylog.runMyLog()

    def writeText(self,filename,var):
        with open(filename, 'w') as f:  # 打开test.txt   如果文件不存在，创建该文件。
            f.write(str(var))  # 把变量getid写入createactivityid.txt。这里var必须是str格式，如果不是，则可以转一下。
            self.outPutMyLog("将[%s]写入文件[%s]" % (var,filename))

    def readText(self,filename):
        with open(filename,"r+") as f1:
            for line in f1:
                sxhdmcinputtext =line
                self.outPutMyLog("将文件[%s]中第一行内容【%s】返回" % (filename,sxhdmcinputtext))
                return sxhdmcinputtext


    def createdir(self,filedir):
        filelist = filedir.split("/")
        long = len(filelist)
        zuhefiledir = filelist[0]
        for i in range(1,long):
            zuhefiledir = zuhefiledir+"/"+filelist[i]
            if os.path.exists(zuhefiledir):
                self.outPutMyLog("已经存在目录：%s" % zuhefiledir)
            else:
                os.mkdir(zuhefiledir)
                self.outPutMyLog("已经创建目录：%s" % zuhefiledir)

if __name__  == '__main__':
    gettimestr = GetTimeStr()
    gettimestr.writeText("1.txt",'1')
    gettimestr.readText("1.txt")