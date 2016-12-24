# coding=utf8
from BaseMatch import BaseMatch, RenderURL
from app.config import URLBASE
class Bind(BaseMatch):
    def __init__(self,isActive, user, data, dataType, args, **etc):
        super(Bind, self).__init__(isActive, user, data, dataType, args, **etc)

    def GetResult(self):
        url = URLBASE + 'bind?user=' + self.user
        return self.Result(RenderURL(url,"点击此处绑定账号"))