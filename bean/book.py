from sqlalchemy import Column, String, Float, Date, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Company(Base):

    __tablename__ = "company"

    company_id = Column(Integer, primary_key=True)
    company_full_name = Column(String(100), nullable=False)
    company_short_name = Column(String(50))
    company_logo = Column(String(200))
    city = Column(String(20), nullable=False)
    industry_field = Column(String(100))
    company_features = Column(String(200))
    finance_stage = Column(String(8))
    company_size = Column(String(15))
    interview_remark_num = Column(Integer)
    position_num = Column(Integer)
    update_time = Column(Date)
    process_rate = Column(Integer)
    approve = Column(Integer)
    company_combine_score = Column(Float)
    is_has_valid_position = Column(Integer)
    other_label = Column(String(200))
    match_score = Column(Float)


class Jobs(Base):

    __tablename__ = "jobs"

    company_id = Column(Integer, primary_key=True)
    position_id = Column(String(10), nullable=False)
    job_nature = Column(String(5), nullable=False)
    finance_stage = Column(String(50), nullable=False)
    company_name = Column(String(20), nullable=False)
    company_full_name = Column(String(40), nullable=False)
    company_size = Column(String(20), nullable=False)
    industry_field = Column(String(50), nullable=False)
    position_name = Column(String(80), nullable=False)
    city = Column(String(10), nullable=False)
    create_time = Column(Date)
    salary = Column(String(20), nullable=False)
    work_year = Column(String(10), nullable=False, default='不限')
    education = Column(String(10), nullable=False)
    position_advantage = Column(String(100))
    company_label_list = Column(String(400))
    user_id = Column(String(10), nullable=False)
    company_logo = Column(String(100))
    district = Column(String(20), nullable=False, default='北京')
