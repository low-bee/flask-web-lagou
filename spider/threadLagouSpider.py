import threading
import requests
import re
from queue import Queue
import os
import  logging
import time

from Dao.query import Util
from bean.book import Company


class Product(threading.Thread):
    pass


class MyProxy(threading.Thread):

    def __init__(self, proxy_list: Queue, url, queue: Queue, num=0):
        super().__init__()
        self.proxy_list = proxy_list
        self.url = url
        self.num = num
        self.queue = queue

    def getProxy(self):
        return self.proxy_list

    def run(self):
        # if self.proxy_list.full():
        #     print("当前代理队列已经满了， 暂时不必加入新的ip")
        #     return
        if self.proxy_list.qsize() <= 8:
            logging.info("开始请求IP， 将ip加入ip队列")
            self.create_ip()
            logging.info("成功将ip加入队列中，当前队列中的IP数量是： " + str(self.proxy_list.qsize()))
        else:
            logging .info("Ip数量已经足够了，不需要新的ip进入啦！！")

    def create_ip(self):
        try:
            ip_addr, port = self.get_proxy()
            proxy = {
                "http": "http://{}:{}".format(ip_addr, port),
                "https": "http://{}:{}".format(ip_addr, port)
            }
            self.proxy_list.put([proxy, 0])
        except Exception as ec:
            logging.error("")

    def get_proxy(self):
        try:
            response = requests.get(self.url)
            print(response.json())
            ip = response.json()["RESULT"][0]['ip']
            port = response.json()["RESULT"][0]['port']
            return ip, port
        except Exception as ec:
            print(ec)


class Customer(threading.Thread):

    def __init__(self, thread_id, queue, header, proxy: list, proxy_queue:Queue):
        super().__init__()
        self.thread_id = thread_id
        self.queue = queue
        self.header = header
        self.proxy = proxy
        self.proxy_list = proxy_queue

    def run(self) -> None:
        print('启动线程：', self.name)
        self.crawl_spider()
        print('退出了该线程：', self.name)

    def crawl_spider(self):
        while True:
            if self.queue.empty():
                break
            else:
                company_id = self.queue.get().company_id
                self.create_dir("./data/jobs/{}/".format(company_id))
                try:
                    cookie, header = self.__getCookiesByCompanyId(company_id)
                    response = self.__postDataAndCookies(cookie, header, self.proxy[0], company_id, 0)
                except Exception as e:
                    print("thread " + self.name + " dead!! Error: " + str(e))
                    self.proxy[1] += 1
                    self.queue.put(Company(company_id=company_id))
                    self.test_proxy()
                    return

                end = self.calculation_page(response)

                for j in range(1, end+2):
                    print("current thread: " + self.name + ", try url: " + str(company_id)+", pageNo is: "+str(j))
                    # 更新cookies和header
                    if j % 10 == 0:
                        cookies, header = self.__getCookiesByCompanyId(company_id)

                    try:
                        response = self.__postDataAndCookies(cookie, header, self.proxy[0], company_id, j)
                    except Exception as e:
                        print("thread " + self.name + " dead!! Error: " + str(e))
                        self.proxy[1] += 1
                        self.queue.put(Company(company_id=company_id))
                        self.test_proxy()
                        return
                    # 得到的信息如果字符大于100，保存这个文件
                    if len(response.text) >= 100:
                        self.save(response, j, company_id)
                    time.sleep(1)

    def test_proxy(self):
        if self.proxy[1] <= 10:
            self.proxy_list.put(proxy)

    @staticmethod
    def calculation_page(response):
        end = 30
        # 计算公司招聘职位页数
        text = re.search("\"totalCount\":\"(.*)\",", response.text)
        jobs_num = text.group(1) if text is not None else "10"
        page_no = eval(jobs_num) / 10
        if end != int(page_no):
            end = 300 if int(page_no) > 300 else int(page_no)
        return end

    @staticmethod
    def __postDataAndCookies(cookies: dict,
                             header,
                             proxy,
                             company_id,
                             page_no,
                             city="",
                             salary="",
                             work_year="",
                             school_job=""):
        search_position = "https://www.lagou.com/gongsi/searchPosition.json"
        data = {
            "companyId": "{}".format(company_id),
            "positionFirstType": "全部",
            "city": city,
            "salary": salary,
            "workYear": work_year,
            "schoolJob": school_job,
            "pageNo": page_no,
            "pageSize": "10"
        }
        position_resp = requests.post(search_position, data=data, headers=header, cookies=cookies, proxies=proxy)
        return position_resp

    def __getCookiesByCompanyId(self, company_id):
        """
        通过公司Id返回请求公司的构造信息
        :param company_id: 公司ID
        :return:
        """
        company_url = 'https://www.lagou.com/gongsi/j{id}.html'.format(id=company_id)
        home_resp = requests.get(company_url, headers=self.header, proxies=self.proxy[0], allow_redirects=False)
        cookies = home_resp.cookies.get_dict()

        header = self.__setHeaders(company_url, self.header, home_resp)

        return cookies, header

    @staticmethod
    def __setHeaders(company_url, header, home_resp):
        text = re.search(r"window.X_Anti_Forge_Token = '(.*?)'", home_resp.text)
        header['X_Anti_Forge_Token'] = "0" if text is None else text.group(1)
        text = re.search(r"window.X_Anti_Forge_Code = '(.*?)'", home_resp.text)
        header['X_Anti_Forge_Code'] = "None" if text is None else text.group(1)

        header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        header['Referer'] = company_url
        return header

    def save(self, response, n, company_id):
        with open("data/jobs/{}/{}.txt".format(company_id, n), "w", encoding="utf-8") as f:
            f.write(response.text)
            print("成功存入")

    @staticmethod
    def create_dir(path):
        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def get_proxy():
        try:
            response = requests.get(url)
            print(response.json())
            ip = response.json()["RESULT"][0]['ip']
            port = response.json()["RESULT"][0]['port']
            return ip, port
        except Exception as ec:
            print(ec)


if __name__ == '__main__':
    proxy_queue = Queue(20)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75Safari/537.36",
        "host": "www.lagou.com",
        "referer": "https://www.lagou.com/gongsi/62.html"
    }

    session = Util.getDBSession("root", "chuanzhi", "lagou")()
    company_list = list(set(Util.selectAllCompany(session)))
    session.close()
    company_queue = Queue()
    for company in company_list:
        company_queue.put(company)

    url = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=38a390fbdff2441ba08a5877eeb23a9f&orderno=YZ202011133421HESY8K&returnType=2&count=1"

    i = 0
    while not company_queue.empty():
        MyProxy(proxy_queue, url, company_queue).start()
        try:
            i += 1
            if not proxy_queue.empty():

                while True:
                    proxy = proxy_queue.get()
                    if proxy[1] <= 10:
                        break

                Customer(i, company_queue, headers, proxy, proxy_queue).start()

            time.sleep(5)
        except Exception as E:
            print(E)
