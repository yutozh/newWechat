# coding=utf8
from BaseMatch import BaseMatch
import sys
from app.config import ADMINCOMMAND
from app import r
import time

reload(sys)
sys.setdefaultencoding("utf8")

# 管理员上传照片模块
class PhotoAdmin(BaseMatch):
    '''
    step1:管理员发送[管理员上传]
    step2:输入口令
    step3:上传图片
    step4:输入学生信息
    step5:重复3,4步骤， 或输入[退出]
    '''
    def __init__(self, isActive, user, data, dataType, args, **etc):
        super(PhotoAdmin, self).__init__(isActive, user, data, dataType, args, **etc)
        self.echoExit = "\n----------------" \
                        "\n回复“退出”可退出当前状态"
    def GetResult(self):
        if self.isWantToExit():
            return self.Result("已退出上传照片模式～")
        if not self.isActive:
            self.SetTargetAndArgs(self.__class__.__name__, "1")
            self.SetActive()
            return self.Result("请输入管理员口令~"+self.echoExit)
        else:
            self.SetActive()
            if self.GetTargetArgs() == "1":
                if self.data == ADMINCOMMAND:
                    self.SetTargetAndArgs(self.__class__.__name__, "2")
                    return self.Result("验证成功，请开始上传图片")
                else:
                    self.SetTargetAndArgs(self.__class__.__name__, "1")
                    return self.Result("验证失败，请重试"+self.echoExit)
            elif self.GetTargetArgs() == "2":
                if self.dataType == 'image':
                    self.SetTargetAndArgs(self.__class__.__name__,
                                          "3"+"|" + self.data)
                    return self.Result("图片上传成功，接下来请输入学生信息“学号+姓名缩写”\n"
                                "(如：2016308866666xyz)")
                else:
                    return self.Result("上传格式有误，请重试")
            elif self.GetTargetArgs().startswith("3|"):
                if self.dataType == "text":
                    try:
                        stuNumber = self.data[:13]
                        stuName = self.data[13:]
                    except:
                        return self.Result("学生信息输入有误，请重试")
                    if stuNumber.isdigit() and stuName.isalpha():
                        mediaID = self.GetTargetArgs().split('|')[1]
                        r.hset("Photos", self.data, mediaID+"|"+str(time.ctime()))
                        self.SetTargetAndArgs(self.__class__.__name__, "2")
                        return self.Result("录入成功，请上传下一张照片～"+self.echoExit)
                    else:
                        return self.Result("学生信息输入有误，请重试")
                else:
                    return self.Result("请输入正确的学生信息"+self.echoExit)
            else:
                self.SetInactive()
                return self.Result("系统出错，请重试")