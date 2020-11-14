import requests
from requests import Response
from Dao.query import Util


def getDetail(job_id: int, show_id) -> Response:

    url = 'https://www.lagou.com/jobs/{}.html?source=pl&i=pl-0&show={}'.format(job_id, show_id)

    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.424\
        0.75 Safari/537.36'

    }

    response = requests.get(url)
    return response


if __name__ == '__main__':
    session = Util.getDBSession("root", "chuanzhi", "lagou")()
    position_list = Util.queryJobPosition(session)
    for i in position_list:
        getDetail(i[0])
        session.close()
        break
