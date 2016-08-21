# coding=utf8
from redisControl import SetRedis, GetRedis
import logging
import time
from app.config import  ACTIVEDURATION, FUNCTAGSTR, ZIPSTR

# 所有匹配模块的基类
class BaseMatch(object):
    # 类变量，回复消息的类型
    typeList = ["text", "image", "voice", "video", "music", "news"]

    #参数分别是：是否活跃，用户名，数据，消息类型，匹配参数，其他参数
    def __init__(self, isActive, user, data, dataType, args, **etc):
        self.isActive = isActive
        self.user = user
        self.data = data
        self.dataType = dataType
        self.args = args if args != '' else '1'
        self.etc = etc

        # 退出当前状态的字符串，可修改
        self.exitStr = '退出'

    # 设置匹配参数（target），使该用户下次能找到该模块，并带上前一次的参数
    def SetTargetAndArgs(self, matchName, args):
        try:
            SetRedis("User:" + self.user, "target",FUNCTAGSTR+matchName, args)
            return True
        except Exception, e:
            logging.error(e.message)
            return False

    # 获取前一次记录的匹配参数，还原用户状态
    def GetTargetArgs(self):
        try:
            return GetRedis("User:" + self.user, "target").split(ZIPSTR)[1]
        except Exception,e:
            logging.error(e.message)
            return ''

    # 设置其他状态
    def SetOthers(self, name, key, value):
        try:
            SetRedis(name, key, value)
            return True
        except Exception, e:
            logging.error(e.message)
            return False

    # 将用户设置为非活跃
    def SetInactive(self):
        try:
            SetRedis("User:" + self.user, "active", str(int(time.time())-ACTIVEDURATION))
            return True
        except Exception, e:
            logging.error(e.message)
            return False

    # 将用户设置为活跃
    def SetActive(self):
        try:
            SetRedis("User:" + self.user, "active", str(int(time.time())))
            return True
        except Exception, e:
            logging.error(e.message)
            return False

    # 判断输入是否为退出关键字，若是则设置非活跃
    def isWantToExit(self):
        try:
            if self.data == self.exitStr:
                self.SetInactive()
                return True
            else:
                return False
        except Exception, e:
            logging.error(e.message)
            return True

    # 构造返回值列表，第一项为数据，第二项为消息类型
    def Result(self, value, type=0):
        return [value, BaseMatch.typeList[int(type)]]