import os
import time

from Dao.query import Util

if __name__ == '__main__':
    # os.listdir("../spider/data/companyPage/")
    # print(time.time())
    # print(list(os.listdir("../spider/data/companyPage/2/")))
    session = Util.getDBSession("root", "chuanzhi", "lagou")()
    if Util.getCompanyId(62, session=session).count() == 0:
        print("wujieguo")
    session.close()

