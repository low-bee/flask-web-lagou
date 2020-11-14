from myError.MyError import MyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy import func

from bean.book import Company, Jobs


class Util(object):

    @staticmethod
    def testDB(username, password, db_name):
        if type(username) != str:
            MyError.ifNotStr()
        if type(password) != str:
            MyError.ifNotStr()
        if type(db_name) != str:
            MyError.ifNotStr()
        return True

    @staticmethod
    def getDBSession(username: str, password: str, db_name: str):
        try:
            if Util.testDB(username, password, db_name):
                engine = create_engine(
                    "mysql+mysqlconnector://" + username + ":" + password + "@" + "127.0.0.1:3306/" + db_name)
                return sessionmaker(bind=engine)
        except Exception as e:
            print(e)

    @staticmethod
    def selectAllCompany(session: Session):
        return session.query(Company.company_id).filter().all()

    @staticmethod
    def addJobsToDataBase(session, li):
        session.add_all(li)
        session.commit()

    @staticmethod
    def queryJobPosition(session: Session):
        return session.query(Jobs.position_id).all()

    @staticmethod
    def threeParm(company, session: Session):
        jobs = session.query(Jobs.company_name, Jobs.position_name, Jobs.company_label_list).filter(Jobs.company_name ==
                                                                                                    company).all()
        return jobs

    @staticmethod
    def getBar(company, session: Session):
        city = session.query(Jobs.city, func.count('*')).filter(Jobs.company_name == company).group_by(Jobs.city).all()
        return city

    # @staticmethod
    # def getCompanyCityData(company, city, session: Session):
    #     data = session.query(Jobs.position_name, Jobs.job_nature, Jobs.finance_stage, Jobs.salary, Jobs.work_year,
    #                          Jobs.education, Jobs.position_id).filter(Jobs.city == city, Jobs.company_name == company)
    #     return data

    @staticmethod
    def getCompanyCityData(company, city, page_no, page_size, session: Session):
        data = session.query(Jobs.position_name, Jobs.job_nature, Jobs.finance_stage, Jobs.salary, Jobs.work_year,
                             Jobs.education, Jobs.position_id).filter(Jobs.city == city, Jobs.company_name == company) \
            .limit(page_size).offset((page_no - 1) * page_size)
        return data

    @staticmethod
    def getCompanyNum(company, city, session: Session):
        print(session.query(func.count("*")).filter(Jobs.company_name == company).one())
        return session.query(func.count("*")).filter(Jobs.company_name == company, Jobs.city == city).one()[0]

    @staticmethod
    def getCompanyId(id, session: Session):
        return session.query(Company.company_id).filter(Company.company_id == id)
