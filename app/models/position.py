from app.database import BASE
from sqlalchemy import Column, Integer, String


class KoreaPosition(BASE):

    __tablename__ = 'korea_position'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address_lev1 = Column(String(50), nullable=False)
    address_lev2 = Column(String(50), nullable=True)
    address_lev3 = Column(String(50), nullable=True)
    position_x = Column(String(50), nullable=False)
    position_y = Column(String(50), nullable=False)
