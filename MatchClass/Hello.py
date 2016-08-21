# coding=utf8
from BaseMatch import BaseMatch
class Hello(BaseMatch):
    def __init__(self,isActive, user, data, dataType, args, **etc):
        super(Hello, self).__init__(isActive, user, data, dataType, args, **etc)

    def GetResult(self):
        if self.isWantToExit():
            return self.Result("欢迎状态已退出～")
        if not self.isActive:
            self.SetTargetAndArgs(self.__class__.__name__, '1')
            self.SetActive()
            return self.Result("你好，这里是涛～的微信公众号，欢迎关注")
        else:
            self.SetTargetAndArgs(self.__class__.__name__,  str(int(self.args)+1))
            self.SetActive()
            return self.Result("你在5分钟之内找过我，我还记得你, 状态{}".format(self.args))