import sys
from WxPost import WXPost
from Weather import Weather
from Pylog import LogInfo, LogErr, LogWarn
from Holiday import Holiday
from News import News
from CityOil import CityOil
Wxcorpid = ""
Wxcorpsecret = ""


def WxPostRun(wx):
    """
    推送消息至微信Run
    参数：WXPost()的对象
    """
    weather = Weather()
    weather_string = weather.GetWeatherInfo("江苏省", "无锡市", "day")

    holiday = Holiday()
    holiday_string = holiday.IsHoliday(holiday.GetHolidayInfo())

    new = News()
    news_string = new.GetNewsInfo()

    oil = CityOil("jiangsu","wuxi")
    oil_string = oil.GetOilInfo()
    msg = " ---------每日工作提醒---------\n" + holiday_string + weather_string + news_string + oil_string
    wx.SendMessage("text", "@all", msg)


def Ds120jPowerONRun(wx):
    """
    群辉开机时跑的Run
    参数：WXPost()的对象
    """
    msg = "ds120j开机成功"
    wx.SendMessage("text", "@all", msg)


def Ds120jPowerOFFRun(wx):
    """
    群辉关机时跑的Run
    参数：WXPost()的对象
    """
    msg = "ds120j正在关机"
    wx.SendMessage("text", "@all", msg)


if __name__ == "__main__":
    LogInfo("len(args)=" + str(len(sys.argv)))

    if len(sys.argv) >= 2:
        parm = sys.argv[1]
        wx = WXPost()
        wx.corpid = Wxcorpid
        wx.corpsecret = Wxcorpsecret
        wx.agentid = 1000002
        wx.GetToken()
        # 判断第二个参数
        if parm == "PowerOn":
            Ds120jPowerONRun(wx)
        elif parm == "PowerOff":
            Ds120jPowerOFFRun(wx)
        elif parm == "WxPost":
            WxPostRun(wx)
