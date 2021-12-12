import requests
import json
from time import localtime, time
import os
from Pylog import LogWarn, LogErr, LogInfo

class Holiday:
    tm_year = 0  # 几年
    tm_mon = 0  # 几月
    tm_mday = 0  # 几日
    tm_hour = 0  # 几点
    tm_wday = 0  # 礼拜几
    holidays = []

    def GetToday(self):
        localtimes = localtime(time())
        self.tm_year = localtimes[0]  # 几年
        self.tm_mon = localtimes[1]  # 几月
        self.tm_mday = localtimes[2]  # 几日
        self.tm_hour = localtimes[3]  # 几点
        self.tm_wday = localtimes[6]  # 礼拜几

    def GetHolidayInfo(self):
        """
        获取 节假日信息
        http://timor.tech/api/holiday
        """
        self.GetToday()
        if self.tm_mday == 1 and self.tm_year == 1:
            request_url = "http://timor.tech/api/holiday/year"
            headers = {
                "User-Agent": "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25"
            }
            try:
                req = requests.get(request_url, headers=headers)
            except requests.exceptions.ConnectTimeout:
                LogErr("Connect " + request_url + "timeout!")
            except requests.exceptions.ConnectionError:
                LogErr("Connect " + request_url + "Error!")
            else:
                req_js = json.loads(req.text)
                if req_js["code"] == 0:
                    father_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
                    with open(father_path + "/holiday.json", "w+") as f:
                        f.write(json.dumps(req_js, indent=4))
                    f.close()
                    LogInfo("Get HolidayInfo success!")
                    return req_js
                else:
                    LogWarn("Holiday api is bad!")
                    exit()
        else:
            father_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
            with open(father_path + "/holiday.json", "r") as f:
                data = f.read()
            f.close()
            req_js = json.loads(data)
            LogInfo("Get HolidayInfo success!")
            return req_js

    def IsHoliday(self, req_js):
        """
        判断是否为节假日
        """
        holidayinfo = req_js["holiday"]
        tm_str = ""
        holiday_string = (
            str(self.tm_year)
            + "年"
            + str(self.tm_mon)
            + "月"
            + str(self.tm_mday)
            + "日 "
            + "礼拜"
            + str(self.tm_wday + 1)
            + "\n"
        )
        if self.tm_mon < 10:
            tm_str += "0" + str(self.tm_mon) + "-"
        else:
            tm_str += str(self.tm_mon) + "-"
        if self.tm_mday < 10:
            tm_str += "0" + str(self.tm_mday)
        else:
            tm_str += str(self.tm_mday)
        if tm_str in holidayinfo:
            if holidayinfo[tm_str]["holiday"] == True:
                holiday_string += "今天是休息日，好好享受吧！"
            else:
                holiday_string += "今天也要上班哦，早早到公司！"
        else:
            if self.tm_wday <= 4:
                holiday_string += "今天正常上班哦，不要忘了！"
            else:
                holiday_string += "今天是双休中的一天哦，休息休息吧！"
        return holiday_string + "\n"
