import time

def GetLocalTime():
    """
    获取当前格式化的时间并且返回
    """
    localtime = time.asctime(time.localtime(time.time()))
    return localtime


def PrintColor(color, s):
    """
    打印时输出前景色
    color 前景色 如 red
    s 字符串，输出的内容
    """
    color_index = ""
    if color == "red":
        color_index = "31"
    elif color == "green":
        color_index = "32"
    elif color == "yellow":
        color_index = "33"
    print("\033[0;" + color_index + ";40m" + s + "\033[0m")


def LogErr(s):
    """
    格式化打印LogErr
    参数为string类
    """
    PrintColor("red", "ERROR [" + GetLocalTime() + "]    " + s)


def LogWarn(s):
    """
    格式化打印LogWarn
    参数为string类
    """
    PrintColor("yellow", "WARNING [" + GetLocalTime() + "]    " + s)


def LogInfo(s):
    """
    格式化打印LogInfo
    参数为string类
    """
    print("[" + GetLocalTime() + "]    " + s)
