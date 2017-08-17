# coding=utf8
import sys
import hashlib
import time
import logging
from xml.etree import ElementTree
from flask import render_template
from app import r
from Message import Message

reload(sys)
sys.setdefaultencoding("utf-8")

# XML解析
def findNode(rec, node):
    try:
        return rec.self.find(node).text
    except Exception, e:
        print str(e)
        return ""

class BaseWechat(object):
    def __init__(self, token):
        self.token = token
        self.data = ''
        self.fromUser = ''
        self.toUser = ''
        self.timestamp = ''
        self.msgType = ''
        self.msgID = ''

        self.resultContent = ''
        self.resultType = ''

    def findNode(self, node):
        try:
            return self.rec.find(node).text
        except Exception, e:
            print str(e)
            return ""

    # 检验3个参数值是否正确
    def EchoTest(self, signature, timestamp, nonce, echostr):
        listTest = [self.token, nonce, timestamp]
        listTest.sort()
        s = ""
        for x in listTest:
            s += x
        resTest = hashlib.sha1(s).hexdigest()

        if resTest == signature:
            return True
        else:
            return False

    # 解析XML，提取各项信息
    def ParseXML(self, data):
        self.rec = ElementTree.fromstring(data)
        try:
            # xmlObj = ElementTree.fromstring(data)
            self.fromUser = self.findNode("FromUserName")
            self.toUser = self.findNode( "ToUserName")
            self.timestamp = self.findNode("CreateTime")
            self.msgType = self.findNode( "MsgType")
            self.msgID = self.findNode("MsgId")
        except Exception, e:
            print str(e)
            logging.error(str(e))

    # 获取用户当前状态（active,target)
    def __GetUserStatus(self):
        try:
            return r.hgetall("User:" + self.fromUser)
        except Exception, e:
            return False

    # 构造Message类，解析Content部分
    def HandleData(self):
        msg = ""
        if self.msgType == 'text':
            self.data = self.findNode("Content")
            msg = Message(data=self.data,
                          user=self.fromUser,
                          status=self.__GetUserStatus(),
                          dataType='text')

        if self.msgType == 'image':
            self.MediaId = self.findNode("MediaId")
            msg = Message(data=self.MediaId,
                          user=self.fromUser,
                          status=self.__GetUserStatus(),
                          dataType='image')

        self.resultContent = msg.Parse()
        self.resultType = msg.ResType()

    # 根据结果渲染返回值模板
    def RenderResult(self):
        res = 'success'
        if self.resultType == 'text':
            res = render_template("MsgText.xml",
                            toUser=self.fromUser,
                            fromUser=self.toUser,
                            timestamp=str(int(time.time())),
                            resultContent=self.resultContent)

        if self.resultType == 'image':
            res = render_template("MsgPic",
                            toUser=self.fromUser,
                            fromUser=self.toUser,
                            timestamp=str(int(time.time())),
                            media_id=self.resultContent)
        return res

    # 更改用户状态数据
    def SetUserStatus(self, key, value):
        r.hset("User:" + self.fromUser, key, value)

