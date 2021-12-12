import requests
import re
import os
import time


path = os.getcwd()
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }

def requests_get(ac_url):
    r = requests.get(ac_url,headers=headers).text
    print(r)
    if "出错啦！" in r:
        print("并没有找到你想要的信息！")
        return 0
    a = get_informations(r)
    return a

def get_informations(r):
    informations=[]
    filename=''
    p1='';p2='';p3='';p4=''
    urls = re.findall("[a-zA-z]+://[^\s]*",r)
    for url in urls:
        if "tx" in url:
            informations = url.split("{")   
        for information in informations:
            if '1080P' in information:
                p1 = re.findall("[a-zA-z]+://[^\s]*",information)
                p1 = "1080p地址:"+p1[0][0:p1[0].index("\\")]
            elif '超清' in information:
                p2 = re.findall("[a-zA-z]+://[^\s]*",information)
                p2 = "超清地址:"+p2[0][0:p2[0].index("\\")]
            elif "高清" in information:
                p3 = re.findall("[a-zA-z]+://[^\s]*",information)
                p3 = "高清地址:"+p3[0][0:p3[0].index("\\")]
            elif "标清" in information:
                p4 = re.findall("[a-zA-z]+://[^\s]*",information)
                p4 = "标清地址:"+p4[0][0:p4[0].index("\\")]
            # elif "title" in information:
            #     index = information.index("fileName")
            #     filename = information[index+11:information.index("\",\"id\"",index)]
    return p1,p2,p3,p4

def download_m3u8(ipt2):
    print("正在下载m3u8")
    download = ""
    if ipt2 == '1':
        download = a[0][5:]
    elif ipt2=='2':
        download = a[1][5:]
    elif ipt2=='3':
        download = a[2][5:]
    elif ipt2=='4':
        download = a[3][5:]
    else:
        print("输入错误！") 
        return 0
    r = requests.get(download,headers=headers,stream=True).text
    with open(path+"/2.txt","w+") as f:
        f.write(r)
    f.close()
    print("完成")
    return 1


def download_ts():
    with open(path+"/2.txt","r+") as f:
        t = f.readlines()
    f.close()
    print("开始下载---")
    if not os.path.exists(path+"/vedio"):
        os.mkdir(path+"/vedio")
    l=0
    for i in t:
        if i[0]!="#" and len(i)>8:
            s1 = i.split("?")
            s2 = s1[1].split("&")
            s3 = s2[0].split("=")
            s4 = s2[1].split("=")
            params={
                "pkey":s3[1],
                "safety_id":s4[1][:-1]
            }
            download_url = "https://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/segment/"+s1[0]
            # print(download_url)
            r = requests.get(download_url,headers=headers,params=params,stream=True)
            #print(r.url)
            with open(path+"/vedio/"+str(l)+".ts","wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
            f.close()
            print("正在下载{0}.ts".format(l))
            l+=1
            
            time.sleep(1)
    print("下载完成---")

def involve_ts():
    print("合并视频")
    ls = os.listdir(path+"/vedio/")
    print(len(ls))
    contect=""
    for i in range(len(ls)):
        contect += path+"/vedio/"+str(i)+".ts"
        if i != len(ls)-1:
            contect+="|"
    print(contect)
    cmd = "ffmpeg -i concat:\""+contect+"\" -acodec copy -vcodec copy -vbsf h264_mp4toannexb "+path+"/vedio/out.mp4"
    os.system(cmd)
    print("完成")

def remove_ts():
    if os.path.exists(path+"/vedio/out.mp4"):
        time.sleep(5)
        print("删除ts视频")
        ls = os.listdir(path+"/vedio/")
        #判断文件是否存在
        for i in range(len(ls)):
            if(os.path.exists(path+"/vedio/"+str(i)+".ts")):
                os.remove(path+"/vedio/"+str(i)+".ts")
            else:
                print ("要删除的文件不存在！")
        print("完成")

if __name__ == "__main__":
    while True:
        print("|---------------------本程序只供学习，不能用作商业---------------------|")
        ipt = input("请输入你要下载的视频ac:(例ac14856217)")
        ac_url= "https://www.acfun.cn/player/"+ipt
        a = requests_get(ac_url)
        if a == 0:
            continue
        #print("当前视频title："+a[4])
        print(a[0]+"\n")
        print(a[1]+"\n")
        print(a[2]+"\n")
        print(a[3]+"\n")
        while True:
            print("Which do you want to download?")
            print("1：1080P")
            print("2：超清")
            print("3：高清")
            print("4：标清")
            ipt2 = input()
            a = download_m3u8(ipt2)
            if a == 0:
                continue
            if a == 1:
                download_ts()
                involve_ts()
                remove_ts()
            break
        break
        print("|---------------------本程序只供学习，不能用作商业---------------------|")
