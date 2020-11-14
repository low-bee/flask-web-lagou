import json
import os
from datetime import datetime
import time

from bean.book import Company, Jobs
from Dao.query import Util


def getCompanyObject():

    session = Util.getDBSession("root", "chuanzhi", "lagou")()
    for jk in os.listdir("../spider/data/companyPage/"):
        li = list()
        for i in range(1, len(os.listdir("../spider/data/companyPage/{}/".format(jk))) + 1):
            with open("../spider/data/companyPage/{}/{}.txt".format(jk, i), encoding="utf-8") as fp:
                data = json.load(fp)
                for j in data["result"]:

                    try:
                        if j.get("otherLabel", 0) != 0 and j.get("companyFeatures", 0) != 0 and j.get("companyLogo",
                                                                                                      0) != 0 and j.get(
                                "industryField", 0) != 0:
                            company = Company(company_id=j['companyId'], company_full_name=j['companyFullName'],
                                              company_short_name=j['companyShortName'], company_logo=j['companyLogo'],
                                              city=j['city'], industry_field=j['industryField'],
                                              company_features=j['companyFeatures'], finance_stage=j['financeStage'],
                                              company_size=j['companySize'], position_num=j['positionNum'],
                                              interview_remark_num=j['interviewRemarkNum'],
                                              update_time=j['updateTime'], process_rate=j['processRate'],
                                              approve=j['approve'], company_combine_score=j['companyCombineScore'],
                                              is_has_valid_position=j['isHasValidPosition'],
                                              other_label=j['otherLabel'], match_score=j['matchScore']
                                              )

                        else:
                            company = Company(company_id=j['companyId'], company_full_name=j['companyFullName'],
                                              company_short_name=j['companyShortName'],
                                              city=j['city'], position_num=j['positionNum'],
                                              finance_stage=j['financeStage'], company_size=j['companySize'],
                                              interview_remark_num=j['interviewRemarkNum'],
                                              update_time=j['updateTime'], process_rate=j['processRate'],
                                              approve=j['approve'], company_combine_score=j['companyCombineScore'],
                                              is_has_valid_position=j['isHasValidPosition'],
                                              match_score=j['matchScore']
                                              )
                        if test_company(company, li, session):
                            li.append(company)
                    except Exception as e:
                        print(e)
        Util.addJobsToDataBase(session, li)
    session.close()


def getJobObject(company_id):
    session = Util.getDBSession("root", "chuanzhi", "lagou")()
    path = "../spider/data/jobs/{}/".format(company_id)
    name_list = os.listdir(path)
    for i in name_list:
        with open(path+i, encoding="utf-8") as fp:
            try:
                data = json.load(fp)
            except Exception as e:
                print(e)
                return
            li = list()
            if data.get("content", False):
                for j in data["content"]["data"]["page"]["result"]:
                    if j.get("district", False) and j.get('industryField', False) and j.get("companyLogo", False) and j.get("positionAdvantage", False):
                        jobs = Jobs(company_id=j['companyId'], position_id=j['positionId'], job_nature=j['jobNature'],
                                    finance_stage=j['financeStage'], company_name=j['companyName'],
                                    company_full_name=j['companyFullName'], company_size=j['companySize'],
                                    industry_field=j['industryField'], position_name=j['positionName'], city=j['city'],
                                    create_time=datetime.now(), salary=j['salary'], work_year=j['workYear'],
                                    education=j['education'], position_advantage=j['positionAdvantage'],
                                    company_label_list=",".join(j['companyLabelList']), user_id=j['userId'],
                                    company_logo=j['companyLogo'], district=j['district']
                                    )
                        li.append(jobs)
            Util.addJobsToDataBase(session, li)

        print(i)
        print("--" * 50)
    return li


def file_path(path):
    for company_id in os.listdir(path):
        for li in os.listdir(path + "/{}".format(company_id)):
            for i in li:
                file_name = path + "/{}".format(company_id) + "/{}.txt".format(i)
                if os.path.getsize(file_name) < 5 * 1024:
                    del_small_file(file_name)


def del_small_file(file_name):
    size = os.path.getsize(file_name)
    file_size = 5 * 1024
    if size < file_size:
        print("remove: ", size, file_name)
        os.remove(file_name)


def test_company(company: Company, li, session):

    for i in li:
        if company.company_id == i.company_id:
            return False

    if Util.getCompanyId(company.company_id, session=session).count() != 0:
        return False

    return True


if __name__ == '__main__':
    # # save company detail
    # companyObjectList = getCompanyObject(1, 64)
    # session = Util.getDBSession("root", "chuanzhi", "lagou")()
    # getCompanyObject()

    # file_path("../spider/data/jobs")

    lis = list(map(eval, os.listdir("../spider/data/jobs/")))
    lis.sort()

    for i in lis:
        length = len(os.listdir("../spider/data/jobs/{}/".format(i)))
        if length > 0:
            jobs = getJobObject(i)
