# coding=utf8
from BaseMatch import BaseMatch
import requests
import xmltodict
import sys
import logging

reload(sys)
sys.setdefaultencoding("utf8")

class Weather(BaseMatch):
    def __init__(self, isActive, user, data, dataType, args, **etc):
        super(Weather, self).__init__(isActive, user, data, dataType, args, **etc)

    def GetResult(self):
        if self.isWantToExit():
            return self.Result("已退出查询天气模式")
        if not self.isActive:
            self.SetTargetAndArgs(self.__class__.__name__, '1')
            self.SetActive()
            return self.Result("请输入城市名称～")
        else:
            self.SetActive()
            try:
                return self.Result(self.GetWeather(self.data) +
                               "\n回复“退出”可退出查询天气模式～")
            except Exception, e:
                logging.error(e.message)
                self.SetInactive()
                return self.Result("系统错误")

    def GetWeather(self, city):
        # city_code = urllib2.quote(city)
        cityGB = city.encode("gb2312")
        day = [{}, {}]

        for i in [0,1]:
            params ={"city":cityGB, "password":"DJOYnieT8234jlsK", "day":str(i+1)}
            r = requests.get("http://php.weather.sina.com.cn/xml.php", params=params)
            r.encoding = "utf-8"
            xml = xmltodict.parse(r.text)
            xmlMain = xml["Profiles"]
            if not xmlMain:
                return "你输入的城市有误,请输入正确的城市名称～"
            xmlWeather = xmlMain["Weather"]

            day[i]["day_weather"] = xmlWeather["status1"]
            day[i]["night_weather"] = xmlWeather["status2"]
            day[i]["date"] = xmlWeather["savedate_weather"]
            day[i]["temperature1"] = xmlWeather["temperature1"]
            day[i]["temperature0"] = xmlWeather["temperature2"]

        d = ["", ""]
        for i in [0,1]:
            d[i] = "({d}):\n[白天] {w1}|[夜晚] {w2}\n气温{t1}℃-{t2}℃".format(
                d=day[i]["date"],
                w1=day[i]["day_weather"],
                w2=day[i]["night_weather"],
                t1=day[i]["temperature0"],
                t2=day[i]["temperature1"])

        line = "----------------"
        res = "{c}天气\n" \
              +line+\
              "明天{d1}\n" \
              +line+\
              "后天{d2}"
        res = res.format(
            c=city, d1=d[0], d2=d[1])

        return res