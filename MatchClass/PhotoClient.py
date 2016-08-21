# coding=utf8
from BaseMatch import BaseMatch
import sys
from app import r

reload(sys)
sys.setdefaultencoding("utf8")

# 用户获取照片模块
class PhotoClient(BaseMatch):
    '''
    step1：用户输入[爆照]
    step2：用户输入“学号+姓名缩写”
    即可获取照片
    '''
    def __init__(self, isActive, user, data, dataType, args, **etc):
        super(PhotoClient, self).__init__(isActive, user, data, dataType, args, **etc)

    def GetResult(self):
        if self.isWantToExit():
            return self.Result("已取消照片查询～")
        if not self.isActive:
            self.SetTargetAndArgs(self.__class__.__name__, "1")
            self.SetActive()
            return self.Result("请输入你的“学号+姓名缩写”，获取照片\n"
                               "(如：2016308866666xyz)")
        else:
            if self.dataType == 'text':
                try:
                    stuNumber = self.data[:13]
                    stuName = self.data[13:]
                except:
                    return self.Result("信息输入有误，请重试")
                if stuNumber.isdigit() and stuName.isalpha():
                    mediaID = r.hget("Photos",self.data).split("|")[0]
                    if mediaID is not None:
                        self.SetTargetAndArgs(self.__class__.__name__, "1")
                        return self.Result(mediaID, 1)

                return self.Result("信息输入有误或照片未被上传，请重试\n"
                                   "回复“退出”取消查询")
            else:
                self.Result("请输入正确的学生信息\n"
                            "回复“退出”取消查询")