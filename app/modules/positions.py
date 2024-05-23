import os
import math
import numpy as np
import pandas as pd

from app.database import SESSION
from app.models.position import KoreaPosition


# ========================================================
# 국가 등의 좌표 기능을 모아둔 클래스
# @Author: Lee su-yeon
# @Date: 2024-05-23
# ========================================================
class Positions:

    # ========================================================
    # 생성자
    # ========================================================
    def __init__(self):
        self.session = SESSION
        self.korea_position = f'{os.getcwd()}/app/dataset/korea_lat_lon.xlsx'

    # ========================================================
    # 데이터베이스 입력을 위해 pandas를 이용해
    # 데이터를 불러들인 후 Dictionary형태로 반환
    # ========================================================
    def get_dataset_positions(self, dataset_type):
        if dataset_type == 'korea':
            data_frame = pd.read_excel(self.korea_position)

        insert = []

        for idx in range(len(data_frame)):
            data = {
                'address_lev1': data_frame.values[idx][0],
                'address_lev2': self.convert_nan_to_none(data_frame.values[idx][1]),
                'address_lev3': self.convert_nan_to_none(data_frame.values[idx][2]),
                'position_x': data_frame.values[idx][3],
                'position_y': data_frame.values[idx][4]
            }

            # 2,3 레벨의 주소가 null 값인 데이터는 제외하는 코드 추가
            # @@@@@@@@@@@@@@@@@ 추가 코드
            if data['address_lev2'] is None | data['address_lev3'] is None:
                pass
            else:
                insert.append(data)

        return insert

    # ========================================================
    # 국내 지역의 좌표값을 데이터베이스에 저장
    # ========================================================
    def insert_table_korea_position(self, data):
        try:
            insert = [KoreaPosition(**item) for item in data]

            self.session.add_all(insert)
            self.session.commit()

        except Exception as exception:
            self.session.rollback()
            print(f'에러 발생 :: {exception}')

        finally:
            self.session.close()

    # ========================================================
    # 데이터베이스 입력 시 오류 방지를 위해
    # NaN값을 None(Null)으로 변환
    # ========================================================
    def convert_nan_to_none(self, value):
        if isinstance(value, float) and (math.isnan(value) or np.isnan(value)):
            return None

        return value

    # ========================================================
    # 최초 등록인지 검증을 위해 Dictionary의 값의 카운트(length),
    # 데이터베이스의 count를 비교함.
    # ========================================================
    def check_first_dataset(self, data_type):
        pass

