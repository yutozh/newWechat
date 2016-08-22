# coding=utf8
import redis
import logging
from app.config import ZIPSTR, FUNCTAGSTR
import time
import sys, getopt

r = redis.StrictRedis()

# 添加指定列表中的key-value
def SetRedis(table, key, value, args=''):
    try:
        if args == '':
            r.hset(table, key=key, value=value + args)
        else:
            r.hset(table, key=key, value=value + ZIPSTR + args)
        return True
    except Exception, e:
        logging.error(e.message)
        return False

# 获取指定列表中的value
def GetRedis(table, key):
    try:
        return r.hget(table, key)
    except Exception, e:
        logging.error(e.message)
        return ''

# 添加匹配关键字
def AddKeyWords(keywords, funName):
    try:
        for i in keywords:
            r.hset("MatchName", i, funName)
        r.hset("MatchName", FUNCTAGSTR + funName, funName)
        print "ok"
        return True
    except Exception, e:
        logging.error(e.message)
        return False

# 删除匹配关键字
def DelKeyWords(keywords, funName):
    try:
        for i in keywords:
            r.hdel("MatchName", i)
        r.hdel("MatchName", FUNCTAGSTR + funName)
        print "ok"
        return True
    except Exception, e:
        logging.error(e.message)
        return False

# AddKeyWords(["管理员上传"], "PhotoAdmin")
# AddKeyWords(["爆照"], "PhotoClient")
# print "".isdigit()

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "df:")
    if len(opts) == 0:
        print "(-d) for delete, [-f] for funName, others for keywords"
    isDel = False
    funName = ''
    for op, value in opts:
        if op == '-d':
            isDel = True
        elif op == '-f':
            funName = value
    try:
        if isDel:
            res = DelKeyWords(args, funName)
        else:
            res = AddKeyWords(args, funName)
    except Exception, e:
        print e.message
        res = False

    if res:
        print "完成"
    else:
        print "失败"
    sys.exit(0)
