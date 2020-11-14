import json
import random
import math

from Dao.query import Util
from bean.book import Jobs


class ServiceUtil(object):

    @staticmethod
    def deal(company: str, position: str, warfare: str):

        session = Util.getDBSession("root", "chuanzhi", "lagou")()

        db_data = Util.threeParm(company, session)
        data = ServiceUtil.dealData(db_data, position, warfare)
        data = ServiceUtil.dealThreeParm(data)
        session.close()
        return data

    @staticmethod
    def dealThreeParm(data: list) -> json:
        # Jobs.company_name, Jobs.position_name, Jobs.company_label_list
        def deal(job):
            d = {
                "position_name": job[1],
            }
            return d
        d = list(map(deal, data))
        return d

    @staticmethod
    def testWarfare(warfare, company_list):
        flag = False
        for i in warfare.strip().split(" "):
            if i in company_list:
                flag = True
                break
        return flag

    @staticmethod
    def dealData(jobs, position, warfare):
        length = len(jobs)
        i = 0
        while i < length:
            if position in jobs[i][1] or ServiceUtil.testWarfare(warfare, jobs[i][2]):
                i += 1
            else:
                jobs.remove(jobs[i])
                length -= 1

        return jobs

    @staticmethod
    def dealGetBar(company, position, welfare):
        session = Util.getDBSession("root", "chuanzhi", "lagou")()
        data = Util.getBar(company, session)
        session.close()
        data.sort(key=lambda x: x[1], reverse=True)
        data = data

        return data

    @staticmethod
    def dealGetBarData(data):
        li = list()
        for i in range(len(data)):
            dic = {
                "name": data[i][0],
                "value": data[i][1]
            }
            li.append(dic)
        return li

    @staticmethod
    def dealCityData(job: Jobs):
        d = {
            'position_name': job.position_name,
            'job_nature': job.job_nature,
            'finance_stage': job.finance_stage,
            'salary': job.salary,
            'work_year': job.work_year,
            'education': job.education,
            'position_id': job.position_id
        }
        return d

    @staticmethod
    def getCityData(company, position, welfare, city):
        session = Util.getDBSession("root", "chuanzhi", "lagou")()
        data = Util.getCompanyCityData(company,
                                       city,
                                       random.randint(1, math.ceil(Util.getCompanyNum(company, city, session)/20)),
                                       20, session)
        data = list(map(ServiceUtil.dealCityData, data))
        session.close()
        return data
