import requests
from lxml import etree
import json
from lxml import etree
import re

class DQB:

    def __init__(self, mobile, password):
        self.mobile = mobile
        self.password = password
        self.__NEEDSTOKEN = None
        self.__userid = None
        self.__session = requests.Session()
    
    def get_login_NEEDSTOKEN(self):
        headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://dqb.yixuewk.com/user/my?_shareId=O2QUPIB748",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
        }
        url = "https://dqb.yixuewk.com/"
        params = {
            "_shareId": "-1",
            "_iframe": "1"
        }
        response = self.__session.get(url, headers=headers, params=params, proxies=False)
        self.__NEEDSTOKEN = response.cookies.get_dict()['NEEDSTOKEN']

    def login(self):
        self.get_login_NEEDSTOKEN()
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://dqb.yixuewk.com",
            "Pragma": "no-cache",
            "Referer": "https://dqb.yixuewk.com/?_shareId=-1&_iframe=1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "X-Token": self.__NEEDSTOKEN,
            "sec-ch-ua": "^\\^Chromium^^;v=^\\^112^^, ^\\^Google",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\\^Windows^^"
        }
        cookies = {
            "NEEDSTOKEN": self.__NEEDSTOKEN,
            "username": "",
            "passname": ""
        }
        url = "https://dqb.yixuewk.com/user/login"
        params = {
            "_shareId": "-1"
        }
        data = {
            "mobile": self.mobile,
            "mtoken": "",
            "method": "ajax",
            "code": self.password,
            "_target": "",
            "_targetType": "reload",
            "type": "accountlogin",
            "openid": ""
        }
        response = self.__session.post(url, headers=headers, cookies=cookies, params=params, data=data)

        self.__NEEDSTOKEN = json.loads(response.text)['data']['NEEDSTOKEN']
        self.__userid = json.loads(response.text)['data']['userid']

    def __get_lesson_info(self):
        headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://dqb.yixuewk.com/user/learn/grade/courses?_shareId=O2QUPIB748",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
        }
        cookies = {
            "username": "",
            "passname": "",
            "NEEDSTOKEN": self.__NEEDSTOKEN,
        }
        url = "https://dqb.yixuewk.com/course/play/form"
        params = {
            "courseId": "258477",
            "source": "user_learn_grade_courses",
            "_shareId": "O2QUPIB748"
        }
        response = self.__session.get(url, headers=headers, cookies=cookies, params=params)
        html = etree.HTML(response.text)
        lessonid = html.xpath("//*[@id='lessonlist']//@data-lessonid")
        self.lessonID = []
        [self.lessonID.append(i) for i in lessonid if i not in self.lessonID]
            
    def __get_vedio_info(self):
        self.__get_lesson_info()
        headers = {
        "Accept": "*/*",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://dqb.yixuewk.com/course/play/form?courseId=258477&source=user_learn_grade_courses&_shareId=O2QUPIB748",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
        }
        cookies = {
            "username": "",
            "passname": "",
            "NEEDSTOKEN": self.__NEEDSTOKEN,
        }
        url = "https://dqb.yixuewk.com/course/lesson/data"
        params = {
            "_shareId": "O2QUPIB748",
            "courseId": "258477",
            "lessonId": "295382",
            "playToken": "",
            "isApi": "0"
        }
        response = self.__session.get(url, headers=headers, cookies=cookies, params=params)
        m3u8_url = str(json.loads(response.text)["lesson"]["mediaUri"])
        return m3u8_url

    def get_vedio_m3u8(self):
        url = self.__get_vedio_info()
        header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        # requests得到m3u8文件内容
        content = requests.get(url,headers=header).text
        with open('vedio_m3u8.txt', 'w') as f:
            f.write(content)
        if "#EXTM3U" not in content:
            print("未获得m3u8的视频链接！")
            return False
        # 获得.ts路径前的路径
        base_url = url.split('?')[0].replace('playlist_eof.m3u8', '')
        # 得到每一个.ts文件
        tslist=re.findall('EXTINF:(.*),\n(.*)\n#',content)
        newlist=[]
        for i in tslist:
            newlist.append(i[1])

        #得到每一个完整视频的链接地址
        tslisturl=[]
        for i in newlist:
            tsurl=base_url+i
            tslisturl.append(tsurl)
        #for循环获取视频文件
        for i in tslisturl:
            res = requests.get(i, header)
            #以追加的形式保存为mp4文件
            with open('./vedio/study.mp4', 'ab+') as f:
                f.write(res.content)
        return True

if __name__ == '__main__':
    user = DQB('13886748038', '12345678') # 此处填入你的账号密码
    user.login()
    user.get_vedio_m3u8()