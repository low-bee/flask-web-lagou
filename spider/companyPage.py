import requests
import re
import time
import os

from Dao.query import Util


def getCookiesByCompanyId(company_id, header):
    """
    通过公司Id返回请求公司的构造信息
    :param company_id: 公司ID
    :param header: 请求头，该请求头https://www.lagou.com/gongsi/j{id}.html的请求头
    :return:
    """
    company_url = 'https://www.lagou.com/gongsi/j{id}.html'.format(id=company_id)
    home_resp = requests.get(company_url, headers=header)
    a = home_resp.headers
    cookies = home_resp.cookies.get_dict()

    header = setHeaders(company_url, header, home_resp)

    return cookies, header


def setHeaders(company_url, header, home_resp):
    text = re.search(r"window.X_Anti_Forge_Token = '(.*?)'", home_resp.text)
    header['X_Anti_Forge_Token'] = "0" if text is None else text.group(1)
    text = re.search(r"window.X_Anti_Forge_Code = '(.*?)'", home_resp.text)
    header['X_Anti_Forge_Code'] = "None" if text is None else text.group(1)

    header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    header['Referer'] = company_url
    return header


def getCompanyShowId(cookie):
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.424\
        0.75 Safari/537.36",
        "referer": "https://www.lagou.com/",
        "cookie": cookie,

    }
    url = "https://www.lagou.com/gongsi/"
    response = requests.get(url, headers=header)
    data_lg_webtj_show_id = re.search("data-lg-webtj-_show_id=\"(.*?)\"", response.text).group(1)
    return data_lg_webtj_show_id, response.headers


def postDataAndCookies(cookies: dict, header, company_id, pageNo):
    search_position = "https://www.lagou.com/gongsi/searchPosition.json"
    data = {
        "companyId": "{}".format(company_id),
        "positionFirstType": "全部",
        "city": "",
        "salary": "",
        "workYear": "",
        "schoolJob": "false",
        "pageNo": pageNo,
        "pageSize": "10"
    }
    position_resp = requests.post(search_position, data=data, headers=header, cookies=cookies)
    return position_resp


def createDir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def save(fp, n, company_id):
    with open("data/jobs/{}/{}.txt".format(company_id, n), "w", encoding="utf-8") as f:
        f.write(fp.text)


if __name__ == '__main__':

    session = Util.getDBSession("root", "chuanzhi", "lagou")()
    company_list = list(set(Util.selectAllCompany(session)))
    session.close()

    length = len(company_list)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75\
                                Safari/537.36",
        "host": "www.lagou.com",
        "referer": "https://www.lagou.com/gongsi/62.html"
    }

    temp = 0

    for index, k in enumerate(company_list):
        if k.company_id == 120655460:
            temp = index
            break
    print(temp)
    try:
        for i in range(temp, length - temp):
            flag = True
            company_id = company_list[i].company_id
            # 继续运行

            # 按照公司名称创建目录
            createDir("./data/jobs/{}/".format(company_id))

            cookies, headers = getCookiesByCompanyId(company_id, headers)

            response = postDataAndCookies(cookies, headers, company_id, 1)
            end = 30

            # 计算公司招聘职位页数
            text = re.search("\"totalCount\":\"(.*)\",", response.text)

            jobs_num = text.group(1) if text is not None else "10"

            pageNo = eval(jobs_num) / 10

            if end != int(pageNo):
                end = 300 if int(pageNo) > 300 else int(pageNo)

            # 循环获取职位信息
            for j in range(1, end+2):
                # 十次请求更新一次cookie和headers，保持稳定
                if j % 10 == 0:
                    cookies, headers = getCookiesByCompanyId(company_id, headers)
                response = postDataAndCookies(cookies, headers, company_id, j)
                text = response.text
                print("try: " + str(company_id) + " ok plus 1, current company id is " + str(company_id) +
                      ", current num is " + str(j))
                if len(response.text) >= 500:
                    save(response, j, company_id)
                time.sleep(1)

    except Exception as e:
        print(e)
