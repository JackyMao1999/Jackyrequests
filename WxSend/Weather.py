import requests
from Pylog import LogInfo,LogErr,LogWarn
import json


class Weather:
    """
    天气处理类
    """
    def GetWeatherInfo(self,province,city,time):
        """
        获取天气信息
        """
        request_url = "https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province="+province+"&city="+city
        weather_string = ""
        try:
            weather_info = requests.get(request_url).text
        except requests.exceptions.ConnectTimeout:
            LogErr("Connect "+ request_url +"timeout!")
        except requests.exceptions.ConnectionError:
            LogErr("Connect "+ request_url +"Error!")
        else:
            weather_js = json.loads(weather_info) #解析成json格式
            if weather_js['status']!=200:        #判断数据获取是否通畅
                LogWarn("数据源解析错误，请检查数据源是否正确！")
            else:
                LogInfo("Get weather success!")
                weather_string = " -------------天气-------------\n"
                if time == "now":
                    # 获取现在天气的信息
                    degree = weather_js['data']['observe']['degree']                # 温度
                    humidity = weather_js['data']['observe']['humidity']            # 湿度
                    pressure =  weather_js['data']['observe']['pressure']           # 气压
                    weather = weather_js['data']['observe']['weather']              # 天气状况
                    wind_direction = weather_js['data']['observe']['wind_direction']# 风向
                    wind_power = weather_js['data']['observe']['wind_power']        # 风强度 
                    weather_string = weather_string+" 温度:"+degree+" 湿度:"+humidity+" 气压:"+pressure+" 天气状况:"+weather+" 风向:"+wind_direction+" 风强度:"+wind_power+"\n"
                elif time == "day":
                    # 获取当天天气的信息
                    day_weather = weather_js['data']['forecast_24h']["1"]['day_weather']                    # 白天天气
                    day_wind_direction = weather_js['data']['forecast_24h']["1"]['day_wind_direction']      # 白天风向
                    day_wind_power = weather_js['data']['forecast_24h']["1"]['day_wind_power']              # 白天风强度
                    max_degree = weather_js['data']['forecast_24h']["1"]['max_degree']                      # 最高温度
                    min_degree = weather_js['data']['forecast_24h']["1"]['min_degree']                      # 最低温度
                    night_weather = weather_js['data']['forecast_24h']["1"]['night_weather']                # 晚上天气
                    night_wind_direction = weather_js['data']['forecast_24h']["1"]['night_wind_direction']  # 晚上风向
                    night_wind_power = weather_js['data']['forecast_24h']["1"]['night_wind_power']          # 晚上风强度
                    weather_string = weather_string+"白天天气:"+day_weather+"\n风向:"+day_wind_direction+" 风强度:"+day_wind_power+"\n温度:"+min_degree+"-"+max_degree+"\n晚上天气:"+night_weather+"\n风向:"+night_wind_direction+" 风强度:"+night_wind_power+"\n"
                tips = weather_js['data']['tips']['observe']['0']                   # 小贴士
                weather_string = weather_string+"小贴士:"+tips
            return weather_string

