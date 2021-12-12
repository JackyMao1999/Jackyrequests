import requests
from Pylog import LogErr, LogWarn, LogInfo
from bs4 import BeautifulSoup


class News:
    def GetNewsInfo(self):
        """
        获取网易新闻中的今日推荐新闻
        https://news.163.com/domestic/
        """
        request_url = "https://news.163.com/domestic/"
        news_string = " -------------要闻-------------\n"
        try:
            req = requests.get(request_url)
        except requests.exceptions.ConnectTimeout:
            LogErr("Connect " + request_url + "timeout!")
        except requests.exceptions.ConnectionError:
            LogErr("Connect " + request_url + "Error!")
        else:
            soup = BeautifulSoup(req.text, features="html.parser")
            today_newslist = soup.find("div", {"class": "today_news"}).findAll("li")
            for i in range(len(today_newslist)):
                a = today_newslist[i].find("a")
                new_txt = a.get("title")
                new_href = a.get("href")
                news_string += str(i + 1) + '.<a href="' + new_href + '">' + new_txt + "</a>\n"
        LogInfo("Get news success!")
        return news_string
