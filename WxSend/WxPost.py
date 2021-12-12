import requests
from Pylog import LogErr, LogWarn, LogInfo
import json

class WXPost:
    """
    自动推送消息给微信类
    """

    corpid = ""  # 企业微信ID
    corpsecret = ""  # Secret是用于保障数据安全的“钥匙”
    access_token = ""  # 企业微信访问API授权码
    agentid = 0    # 企业应用的id
    def GetToken(self):
        """
        获取企业微信API接口的access_token函数
        https://open.work.weixin.qq.com/api/doc/90000/90135/91039
        """
        request_url = (
            "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + self.corpid + "&corpsecret=" + self.corpsecret
        )

        try:
            req = requests.post(request_url)
        except requests.exceptions.ConnectTimeout:
            LogErr("Connect "+ request_url +"timeout!")
        except requests.exceptions.ConnectionError:
            LogErr("Connect "+ request_url +"Error!")
        else:
            req_js=json.loads(req.text)
            if req_js['errmsg'] == "ok":
                self.access_token = req_js["access_token"]
                LogInfo("Get access_token success!")
            else:
                LogWarn("Get access_token failed!")
            

    def SendMessage(self, msgtype, user, msg):
        """
        发送消息函数
        https://open.work.weixin.qq.com/api/doc/90000/90135/90236#markdown%E6%B6%88%E6%81%AF
        """
        request_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.access_token
        body = {
            "touser": user,
            "msgtype": msgtype,
            "agentid": self.agentid,
            msgtype: {"content": msg},
            "safe": 0,
            "enable_duplicate_check": 0,

            "duplicate_check_interval": 1800
        }
        body_js = json.dumps(body)
        try:
            req = requests.post(request_url, data=body_js)
        except requests.exceptions.ConnectTimeout:
            LogErr("Connect "+ request_url +"timeout!")
        except requests.exceptions.ConnectionError:
            LogErr("Connect "+ request_url +"Error!")
        else:
            req_js=json.loads(req.text)
            if req_js['errmsg'] == "ok":
                LogInfo("SendMessage success!")
            else:
                LogWarn("SendMessage failed!")




