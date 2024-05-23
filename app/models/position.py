from app.database import BASE
from sqlalchemy import Column, Integer, String, Float


class KoreaPosition(BASE):

    __tablename__ = 'dev_positions_korea'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address_lev1 = Column(String(50), nullable=False)
    position_x = Column(Float, nullable=False)
    position_y = Column(Float, nullable=False)