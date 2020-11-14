import requests
import re
import time
import os


def getCookiesByCompanyId(company_id, header):
    """
    通过公司Id返回请求公司的构造信息
    :param company_id: 公司ID
    :param header: 请求头，该请求头https://www.lagou.com/gongsi/j{id}.html的请求头
    :return:
    """
    company_url = 'https://www.lagou.com/gongsi/j{id}.html'.format(id=company_id)
    home_resp = requests.get(company_url, headers=header)
    cookies = home_resp.cookies.get_dict()

    header = setHeaders(company_url, header, home_resp)

    return cookies, header


def setHeaders(company_url, header, home_resp):
    try:
        header['X_Anti_Forge_Token'] = re.search(r"window.X_Anti_Forge_Token = '(.*?)'", home_resp.text).group(1)
        header['X_Anti_Forge_Code'] = re.search(r"window.X_Anti_Forge_Code = '(.*?)'", home_resp.text).group(1)
        header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        header['Referer'] = company_url
    except Exception as e:
        print(e)
    finally:
        header['X_Anti_Forge_Token'] = 'None'
        header['X_Anti_Forge_Code'] = '0'
        header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        header['Referer'] = company_url
    return header


def setHeadersForCompanyId(headers):
    headers['X_Anti_Forge_Token'] = '0',
    headers['X_Anti_Forge_Code'] = 'None',
    headers['x-requested-with'] = 'XMLHttpRequest',
    return headers


def postDataAndCookies(cookies: dict, header, company_id):
    search_position = "https://www.lagou.com/gongsi/searchPosition.json"
    data = {
        "companyId": "{}".format(company_id),
        "positionFirstType": "全部",
        "city": "",
        "salary": "",
        "workYear": "",
        "schoolJob": "false",
        "pageNo": "1",
        "pageSize": "10"
    }
    position_resp = requests.post(search_position, data=data, headers=header, cookies=cookies)
    return position_resp


def getUserTraceToken():
    headers = {
        "referer": "https://www.lagou.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0\
                                    .4240.75 Safari/537.36"
    }
    response = requests.get("https://www.lagou.com/upload/ltm/pageload.html?u=/gongsi/", headers=headers)
    user_trace_token = dict(response.headers)["Set-Cookie"]
    re.search(r"(.*?);", user_trace_token).group(1)
    return user_trace_token


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


def getCompanyId(show_id, cookies, headers, pageNo, city_n):
    data = {
        "first": "false",
        "pn": "{}".format(pageNo),
        "sortField": "0",
        "havemark": "0",
        "showId": show_id
    }
    url = "https://www.lagou.com/gongsi/{}-0-0-0.json".format(city_n)
    response = requests.post(url, data=data, headers=headers, cookies=cookies)
    return response


def save(fp, city, n):
    path = "data/companyPage/{}/".format(city)
    folder = os.path.exists(path)
    if not folder:
        os.mkdir(path)

    with open(path+"{}.txt".format(n), "w", encoding="utf-8") as f:
        f.write(fp.text)


def getCityId(headers):
    city = "北京、上海、广州、深圳、成都、重庆、沈阳、杭州、天津、大连、武汉、苏州、南京、青岛、厦门、西安、宁波、长沙、合肥、郑州、无锡、东莞、济南、" \
           "福州、昆明、长春、哈尔滨、佛山、石家庄、南宁、常州、南昌、呼和浩特、温州、烟台、南通、珠海、贵阳、太原、乌鲁木齐、绍兴、中山、嘉兴、" \
           "唐山、徐州、金华、泉州、洛阳、兰州、海口、吉林、襄阳、汕头、潍坊"
    city_list = city.strip().split("、")

    response = requests.get('https://www.lagou.com/gongsi/allCity.html?option=0-0-0-0', headers=headers)
    text = response.text
    city_num_list = list()
    for city in city_list:
        href = r"https://www.lagou.com/gongsi/(.*?)-0-0-0\">{}</a>".format(city)
        city_num_list.append(re.search(href, text).group(1))
    print(city_num_list)

    return list(zip(city_list, city_num_list))


if __name__ == '__main__':
    try:
        flag = True  #
        user_trace_token = getUserTraceToken()  # 得到参数中的token
        show_id, cookie_parm = getCompanyShowId(user_trace_token)  # 通过token得到show_id和cookie参数

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75\
                            Safari/537.36",
            "host": "www.lagou.com",
            "referer": "https://www.lagou.com/gongsi/62.html"
        }
        city_nums = getCityId(headers)

        # 任意发送一个请求得到 cookie 和 header
        cookies, header = getCookiesByCompanyId(62, headers)
        # company_id_response = getCompanyId(show_id, cookies, headers, 63, 0)

        for city_num in city_nums:
            cookies, header = getCookiesByCompanyId(2474, headers)
            for i in range(1, 64):
                if i % 10 == 0:
                    user_trace_token = getUserTraceToken()
                    show_id, cookie_parm = getCompanyShowId(user_trace_token)
                    headers = {
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                         Chrome/86.0.4240.75Safari/537.36",
                        "host": "www.lagou.com",
                        "referer": "https://www.lagou.com/gongsi/62.html"
                    }
                    cookies, header = getCookiesByCompanyId(2474, headers)

                    headers = {
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                         Chrome/86.0.4240.75Safari/537.36",
                        "host": "www.lagou.com",
                        "referer": "https://www.lagou.com/gongsi/62.html"
                    }
                company_id_response = getCompanyId(show_id, cookies, header, i, city_num[1])

                print("success one: " + company_id_response.text[0:50] + ", current: {}".format(i))
                print("*" * 80)
                if len(company_id_response.text) < 500:
                    break
                save(company_id_response, city_num[1], i)
                time.sleep(2)
    except Exception as e:
        print(e)
