import requests
import re
from Pylog import LogWarn, LogErr, LogInfo


class CityOil:
    province = ""
    city = ""
    def __init__(self, province, city):
        self.province = province
        self.city = city
    def GetOilInfo(self):
        """
        获取当前城市的油价
        """
        request_url = "http://youjia.chemcp.com/"+self.province+"/"+self.city+"shi.html"
        oil_string = " -------------油价-------------\n"
        try:
            req = requests.get(request_url)
            req.encoding = 'gb2312'
            reqinfo = req.text
        except requests.exceptions.ConnectTimeout:
            LogErr("Connect "+ request_url +"timeout!")
        except requests.exceptions.ConnectionError:
            LogErr("Connect "+ request_url +"Error!")
        else:
            LogInfo("Get oil info success!")
            pattern = re.compile(r'<td bgcolor=\"#F2F7FC\"><font color=\"red\">(.*?)</font></td>')
            results = pattern.findall(reqinfo)
            oil_string = oil_string + "89号汽油:" + results[0] + "\n92号汽油:" + results[1] + "\n95号汽油:" + results[2] + "\n0号柴油:" + results[3] + "\n"
            return oil_string

