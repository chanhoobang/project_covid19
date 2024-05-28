from app.database import BASE
from sqlalchemy import Column, Integer, String, Float


class KoreaPosition(BASE):

    __tablename__ = 'covid_position_korea'

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(50), nullable=False)
    position_x = Column(Float, nullable=False)
    position_y = Column(Float, nullable=False)


class GlobalPosition(BASE):

    __tablename__ = 'covid_position_global'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nation = Column(String(50), nullable=False)
    position_x = Column(Float, nullable=False)
    position_y = Column(Float, nullable=False)
