import requests
from lxml import etree
import json
import re
import execjs

class DQB:

    def __init__(self, mobile, password):
        self.mobile = mobile
        self.password = password
        self.__NEEDSTOKEN = None
        self.__session = requests.Session()
    
    def __get_login_NEEDSTOKEN(self):
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
        self.__get_login_NEEDSTOKEN()
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
        response = self.__session.post(url, headers=headers, cookies=cookies, params=params, data=data, proxies=False)

        self.__NEEDSTOKEN = json.loads(response.text)['data']['NEEDSTOKEN']
        self.passname = self.__get_passname()

    def __get_passname(self):
        jscode = open("./passname.js").read()
        context = execjs.compile(jscode)
        passname = context.call("get_passname", self.password)
        return passname

    def __get_user_info(self):
        headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
        }
        cookies = {
            "NEEDSTOKEN": self.__NEEDSTOKEN
        }
        url = "https://dqb.yixuewk.com/"
        response = self.__session.get(url, headers=headers, cookies=cookies, proxies=False)
        html = etree.HTML(response.text)
        script_text = html.xpath("//script/text()")[1]
        reg = re.compile("app\..* = .*;")
        match_list = reg.findall(script_text)
        self.schoolId = match_list[0].split("app.schoolId = ")[1].split(";")[0]
        self.schoolCode = match_list[1].split("app.schoolCode = ")[1].split(";")[0]
        self.userId = match_list[2].split("app.userId = ")[1].split(";")[0]
        self.shareId = match_list[4].split("app.shareId = ")[1].split(";")[0]
        headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://dqb.yixuewk.com/user/login?_target=L3VzZXIvbGVhcm4vZ3JhZGUvY291cnNlcz9fc2hhcmVJZD1PMlFVUElCNzQ4&_shareId=O2QUPIB748",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
        }
        cookies = {
            "username": self.mobile,
            "passname": self.passname,
            "NEEDSTOKEN": self.__NEEDSTOKEN,
        }
        url = "https://dqb.yixuewk.com/user/learn/grade/courses"
        params = {
            "_shareId": self.shareId
        }
        response = self.__session.get(url, headers=headers, cookies=cookies, params=params)
        html = etree.HTML(response.text)
        self.gradeId = html.xpath("//div[@class='community_tab_title vip']/input[@type='hidden']/@value")[0]

    def __get_class_info(self):
        self.__get_user_info()
        headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": f"https://dqb.yixuewk.com/user/learn/grade/courses?_shareId={self.shareId}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
        }
        cookies = {
            "NEEDSTOKEN": self.__NEEDSTOKEN
        }
        url = "https://dqb.yixuewk.com/user/learn/grade/course/list"
        params = {
            "_shareId": self.shareId,
            "gradeId": self.gradeId,
        }
        response = requests.get(url, headers=headers, cookies=cookies, params=params, proxies=False)
        html = etree.HTML(response.json()['html'])
        class_list = html.xpath("//div/p[@class='course_item_title']/text()")
        class_url_list = html.xpath("//li[@class='pc_list']/a/@href")
        class_dict = {}
        index = 0
        for i in class_list:
            class_dict[i] = class_url_list[index]
            index += 1
        self.class_dict = class_dict
        index = 1
        for item in class_dict:
            print(f"{index}."+item)
            index += 1
        print("-------------------------")
        class_name = input("请输入您想要下载的班级课程序号")
        return class_name

    def __which_class(self, index):
        cursor = 1
        for item in self.class_dict:
            if(cursor == int(index)):
                return item
            cursor += 1

    def get_lessons_info(self):
        class_index = self.__get_class_info()
        try:
            class_name = self.__which_class(class_index)
            class_url = "https://dqb.yixuewk.com" + self.class_dict[class_name]
        except KeyError as e:
            return "请输入符合条件的序号"
        headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": f"https://dqb.yixuewk.com/user/learn/grade/courses?{self.shareId}",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
        }
        cookies = {
            "NEEDSTOKEN": self.__NEEDSTOKEN
        }
        url = "https://dqb.yixuewk.com/course/play/form"
        params = {
            "courseId": class_url.split("courseId=")[1].split("&")[0],
            "source": "user_learn_grade_courses",
            "_shareId": self.shareId
        }
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        html = etree.HTML(response.text)
        print("---------------------------")
        lesson_class_list = html.xpath("//div[@class='courseitem playbackLesson font-small text-warp course_child display']/div[@class='playback_title']/text()")
        for i in lesson_class_list:
            if '自测题' in i:
                lesson_class_list.remove(i)
        print(lesson_class_list)

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
            "_shareId": self.shareId,
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
        tslist_url=[]
        for i in newlist:
            tsurl=base_url+i
            tslist_url.append(tsurl)
        #for循环获取视频文件
        for i in tslist_url:
            res = requests.get(i, header)
            #以追加的形式保存为mp4文件
            with open('./vedio/study.mp4', 'ab+') as f:
                f.write(res.content)
        return True

if __name__ == '__main__':
    # mobile = input("请输入手机号码:")
    # password = input("请输入密码:")
    user = DQB(mobile="13886748038", password="12345678") # 此处填入你的账号密码
    user.login()
    user.get_lessons_info()