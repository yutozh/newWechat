# coding=utf8
from app import app
from flask import request
import app.config as config
from app.model.Wechat import BaseWechat
import logging

# 微信消息接口
@app.route('/',methods=["POST","GET"])
def main():
    try:
        signature = request.args.get("signature", "")
        timestamp = request.args.get("timestamp", "")
        nonce = request.args.get("nonce", "")
        echostr = request.args.get("echostr", "")

        # 实例化Wechat类，传入设定在微信后台的token
        wc = BaseWechat(config.token)

        # echostr是微信用来验证服务器的参数，需原样返回
        if echostr:
            if wc.EchoTest(signature,timestamp,nonce,echostr):
                return echostr
            else:
                logging.warning("TokenError")
                return 'TokenFail'

        # 解析XML数据
        wc.ParseXML(str(request.data))

        # 处理XML数据
        wc.HandleData()

        # 渲染返回值模板
        return wc.RenderResult()
    except Exception, e:
        return e.message



