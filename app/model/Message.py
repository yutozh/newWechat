# coding=utf8
import time
from app import r
from app.config import ACTIVEDURATION, ZIPSTR, moduleName, DEFAULTMESSAGE
import logging

class Message(object):
    # 参数分别是：数据，用户名，状态（字典），其他键值对
    def __init__(self, data, user, status, dataType, **etc):
        self.data = data
        self.user = user
        self.status = status
        self.dataType = dataType
        self.etc = etc

        self.result = []
    # 根据是否Active以及data，交付对应处理的类
    def Parse(self):
        try:
            isActive = int(time.time()) - int(self.status["active"]) < ACTIVEDURATION
            # print int(time.time()), int(self.status["active"])
        except:
            isActive = False

        args = ''

        # 活跃则从target中获取关键字，不活跃则从原文本中获取
        if isActive:
            try:
                key = self.status["target"].split(ZIPSTR)[0]
                # 根据回复的关键字找到类名
                className = r.hget('MatchName', key).split(ZIPSTR)[0]
                # 获取参数
                args = self.status["target"].split(ZIPSTR)[1]
            except Exception, e:
                className  = r.hget('MatchName', self.data).split(ZIPSTR)[0]
        else:
            r.hset("User:" + self.user , "target", '')
            className = r.hget('MatchName', self.data)

        if className is not None:
            module = __import__(moduleName + className)
            cls = getattr(module, className) # module对象
            cls = getattr(cls, className) # class对象

            # 实例化
            matchObj = cls(isActive=isActive,
                           user=self.user,
                           data=self.data,
                           dataType=self.dataType,
                           args=args,
                           etc=self.etc)

            self.result = matchObj.GetResult()
            return self.result[0]

        else:
            return self.DefaultResult()

    def ResType(self):
        try:
            return self.result[1]
        except Exception, e:
            logging.error(e.message)
            logging.error(self.result)
            return 'text'

    def DefaultResult(self):
        return DEFAULTMESSAGE
