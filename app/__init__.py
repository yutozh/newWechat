# coding=utf8
from flask import Flask
import logging
import os
import redis
r = redis.StrictRedis(host='localhost', port=6379)

app = Flask(__name__)
app.secret_key = "hahahahahaimpossible!!!"

from app.controller.main import *
from app.controller.web import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename= os.path.join(os.getcwd(),'RUNNING.log'),
                    filemode='w')

