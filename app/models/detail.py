from app.database import BASE
from sqlalchemy import Column, Integer, String, Float


class AgeData(BASE):

    __tablename__ = 'covid_age_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(String(50), nullable=False)
    total_cases = Column(Integer, nullable=False)
    death_cases = Column(Integer, nullable=False)
    data_date = Column(String(50), nullable=False)
    active_cases = Column(Float, nullable=False)
    re_rate = Column(Float, nullable=False)
    re_cases = Column(Float, nullable=False)


class GenderData(BASE):

    __tablename__ = 'covid_gender_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gender = Column(String(50), nullable=False)
    total_cases = Column(Integer, nullable=False)
    death_cases = Column(Integer, nullable=False)
    data_date = Column(String(50), nullable=False)
    active_cases = Column(Float, nullable=False)
    re_rate = Column(Float, nullable=False)
    re_cases = Column(Float, nullable=False)


class KoreaData(BASE):

    __tablename__ = 'covid_korea_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String(50), nullable=False)
    data_date = Column(String(50), nullable=False)
    death_cases = Column(Integer, nullable=False)
    total_cases = Column(Integer, nullable=False)
    active_cases = Column(Float, nullable=False)
    re_rate = Column(Float, nullable=False)
    re_cases = Column(Float, nullable=False)


class GlobalData(BASE):

    __tablename__ = 'covid_global_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nation = Column(String(50), nullable=False)
    data_date = Column(String(50), nullable=False)
    death_cases = Column(Integer, nullable=False)
    total_cases = Column(Integer, nullable=False)
    active_cases = Column(Float, nullable=False)
    re_rate = Column(Float, nullable=False)
    re_cases = Column(Float, nullable=False)

