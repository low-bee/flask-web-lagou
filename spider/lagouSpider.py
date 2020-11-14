import requests
import re
import os
from time import sleep


class Spider(object):

    def __init__(self, url):
        self.url = url

    @staticmethod
    def ready():
        headers = {
            "referer": "https://www.lagou.com/",
            "job-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0\
                    .4240.75 Safari/537.36"
        }
        return headers

    def run(self):

        response = requests.get(self.url)


def get(url):
    return requests.get(url).text


if __name__ == '__main__':

    headers = {
        "referer": "https://www.lagou.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0\
                        .4240.75 Safari/537.36"
    }

    gongsi_id = 62
    home_url = 'https://www.lagou.com/j{id}.html'.format(id=gongsi_id)
    home_resp = requests.get(home_url, headers=headers)
    cookies = home_resp.cookies.get_dict()
    headers['X_Anti_Forge_Token'] = re.search(r"window.X_Anti_Forge_Token = '(.*?)'", home_resp.text).group(1)
    headers['X_Anti_Forge_Code'] = re.search(r"window.X_Anti_Forge_Code = '(.*?)'", home_resp.text).group(1)
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['Referer'] = home_url

    position_ajax = 'https://www.lagou.com/gongsi/searchPosition.json'

    proxy_url = "http://127.0.0.1:59977/getip?price=1&word=&count=1&type=text&detail=false"

    for i in range(1, 30):
        ip = re.findall(r"[.*]+", get(proxy_url))[0]
        proxy = {
            "http": "http://{}/".format(ip),
            "https": "https://{}/".format(ip)
        }
        data = {
            'companyId': gongsi_id,
            'positionFirstType': '全部',
            'schoolJob': False,
            'pageNo': i,
            'pageSize': 10
        }
        try:
            position_resp = requests.post(position_ajax, data=data, headers=headers, cookies=cookies, proxies=proxy)
            print("success + 1")
            print(position_resp.text)
            with open("data/{}/cookie{}.txt".format(str(gongsi_id), i), "w+", encoding="utf-8") as fp:
                fp.write(position_resp.text)
        except Exception as e:
            print(e)
        finally:
            sleep(1)