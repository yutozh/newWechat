# coding=utf-8
import urllib
import urllib2
import new

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
test = '''<xml><ToUserName>2</ToUserName>
<FromUserName>3</FromUserName>
<CreateTime>1348831860</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content>2016308866666xja</Content>
<MsgId>1234567890123456</MsgId>
</xml>'''
test0 = '''<xml><ToUserName>2</ToUserName>
<FromUserName>zyt</FromUserName>
<CreateTime>1348831860</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content>天气</Content>
<MsgId>1234567890123456</MsgId>
</xml>'''
test1 = '''<xml><ToUserName>2</ToUserName>
<FromUserName>3</FromUserName>
<CreateTime>1348831860</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[subscribe]]></Event>
<EventKey>22</EventKey>
</xml>'''
test2= '''
<xml>
 <ToUserName><![CDATA[2]]></ToUserName>
 <FromUserName><![CDATA[3]]></FromUserName>
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[image]]></MsgType>
 <PicUrl><![CDATA[this is a url]]></PicUrl>
 <MediaId><![CDATA[1417417174]]></MediaId>
 <MsgId>1234567890123456</MsgId>
 </xml>
 '''
html = 'http://127.0.0.1:5000'
#html = 'http://4.wx4321.sinaapp.com/'
# html = 'http://182.254.146.38/'
headers={"Content-Type":"text/xml","Cookies":"cookie"}

# token = urllib2.urlopen(html+"?signature=48ef9320b175585c1c96d1aa91cbcd992fd47ee9&echostr=14679828899321855931&timestamp=1502971577&nonce=2692058841")
# res = token.read()
# print res


response = urllib2.Request(url=html,data=test0,headers=headers)  # 使用了POST方法将data上传

url_data = urllib2.urlopen(response)

result = url_data.read()

print result
