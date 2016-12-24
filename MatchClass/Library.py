# coding=utf8
from BaseMatch import BaseMatch
from redisControl import GetRedis, SetRedis
import requests
from bs4 import BeautifulSoup
import re
from app.config import URLBASE

class Library(BaseMatch):
    def __init__(self,isActive, user, data, dataType, args, **etc):
        super(Library, self).__init__(isActive, user, data, dataType, args, **etc)
        self.URL_MORE = URLBASE + 'lib/xj?user=' + user
        self.URL_BIND = URLBASE + 'bind?user=' + user
    def GetResult(self):
        if self.isWantToExit():
            return self.Result("已退出查借阅状态~")
        if not self.isActive:
            res = UserRegi(self.user)
            if not res:
                res = '你还没有绑定账号或绑定的信息有误,' + RenderURL(self.URL_BIND, "点此绑定")
            elif res==1:
                res = '你还没有借书哦...' + '\n ' + RenderURL(self.URL_MORE, "点击此处") + ',查查你喜欢看的书吧~'
            else:
                res = '你借了这些书:\n ' + res + RenderURL(self.URL_MORE, "点击此处") + '可续借 或 查询其他图书'

            return self.Result(res)

# 渲染超链接
def RenderURL(url, text):
    return "<"+'a href="' + url + '">' + text + '</a>'

# 判断用户是否绑定,是,返回已借书列表,否,返回False
def UserRegi(user):
    userAccount = GetRedis("User:" + user, 'Account')
    if userAccount:
        username = userAccount
        password = GetRedis("User:" + user, 'Pass_lib')
        books, status = getLib(username, password)
        # 用户名密码错误
        if "-1" in status:
            return False
        # 没有借书
        if len(books) == 0:
            return 1
        res = ''
        for i,j in zip(books,range(1,len(books)+1)):
            res += str(j) + '.' + i["book"] + '\n作者:' + i["author"] + '\n到期时间:' + i["duetime"] + '\n'
        return res
    else:
        return False

def getLib(id, password, append=[]):
    # 查询借阅以及续借
    # append 表示续借书的编号
    # 返回值book_info 是书籍信息列表
    # {'book': 'author':, 'duetime':}
    # res_append 是状态
    # -1 用户名密码错误
    # -2 已达到续借限制
    # -3 本书不能续借
    # -4 序号错误
    #  0 正常
    url_login = 'http://metalib.lib.whu.edu.cn/pds?func=load-login&url=http://metalib.lib.whu.edu.cn:80/pds'
    url_address = "http://opac.lib.whu.edu.cn/F/?func=bor-info"
    header = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    }
    cookie = {
    'qq%5Flogin%5Fstate':'A5950027D534EE0BAB0FD77B29E5F547'
    }
    cookie2 = {
    'PDS_HANDLE':'1810201501732437486411213163117974',
    'qq%5Flogin%5Fstate':'A83EB6BA2325DB85DE52B8CAC79AFE95'
    }
    data = {
    'func':'login',
    'calling_system':'idp_proxy',
    'term1':'short',
    'selfreg':'',
    'institute':'WHU',
    # 'url':'http%3A%2F%2Fapps.lib.whu.edu.cn%2Fidp_proxy%2Fbor_auth_agent.asp%3Fgoto%3Dhttp%253A%252F%252Fapps%252Elib%252Ewhu%252Eedu%252Ecn%252Fweb%252Flogin%252Easp%253Furl%253Dhttp%25253A%25252F%25252Fwww%25252Elib%25252Ewhu%25252Eedu%25252Ecn%25252Fweb%25252Fdefault%25252Easp%26sp%3Dhttp%253A%252F%252Fwww.hub.calis.edu.cn%253A8090%252Famconsole%252FAuthServices%252F242010%253Fverb%253Dsplogin%26idp%3D242010',
    'bor_id':str(id),
    'bor_verification':str(password)
    }

    html_login = requests.post(url = url_login, headers = header, data = data, cookies = cookie)
    html_address = requests.get(url = url_address, headers = header, cookies = cookie2)

    head = BeautifulSoup(html_login.content)
    psd = head.find_all("body")[0]

    book_info = []
    res_append = []

    pds_handle = re.search("pds_handle=\d*", str(psd))
    if not pds_handle:
        res_append = ["-1"]
        return [book_info, res_append]
    spds_handle = pds_handle.group()

    goto = re.search("(http://opac.lib.whu.edu.*)('; )", str(html_address.content))
    sgoto = goto.group(1).replace('info', 'loan')
    url_final = sgoto + '&' + spds_handle

    html_final = requests.get(url = url_final, headers= header)

    if u'您当前没有任何在借单册' in html_final.content:
        return ['', '0']
    else:
        result = BeautifulSoup(html_final.content)
        table = result.find_all("table")[5]
        tbody = table.find_all("tr")[1:]
        # print tbody
        for i in tbody:
            author = i.find_all("td")[2]
            book = i.find_all("td")[3]
            duetime = i.find_all("td")[5]
            book_info.append({'book':book.text, 'author':author.text, 'duetime':duetime.text})

    if append:
        if max(append) <= len(tbody):
            url_append = sgoto.replace('bor-loan', 'bor-renew-all&renew_selected=Y&adm_library=WHU50')
            for i in append:
                book_id = tbody[int(i)-1].find_all('td')[1].input['name']
                url_append = url_append + '&' + book_id + "=Y"
            # print url_append
            html_append = requests.get(url=url_append, headers=header, cookies=cookie)
            bs = BeautifulSoup(html_append.content)
            appended_result =  bs.find("tr", {"class":"tr1"}).find_all_next("tr")[:len(append)]

            for i in appended_result:
                i = i.text
                if u'已达到续借限制' in i:
                    res_append.append('-2')
                elif u'不能再续借' in i:
                    res_append.append('-3')
                else:
                    res_append.append('0')
        else:
            res_append = ["-4"]  # 越界
    return [book_info, res_append]

# print getLib(2014301610157, 16000)
