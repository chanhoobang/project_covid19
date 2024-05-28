import os
import math
import numpy as np
import pandas as pd
from flask_sqlalchemy.pagination import Pagination

from sqlalchemy import select
from app.database import SESSION


# ========================================================
# 프로젝트에서 공통으로 사용하는 소스 모음
# ========================================================
class Common:

    # ========================================================
    # 데이터베이스 입력을 위해 pandas를 이용해
    # 데이터를 불러들인 후 Dictionary형태로 반환
    # ========================================================
    @staticmethod
    def get_dataset(data_type):
        try:
            if data_type == 'korea_position':
                return pd.read_excel(f'{os.getcwd()}/app/dataset/korea_position.xlsx')
            elif data_type == 'global_position':
                return pd.read_csv(f'{os.getcwd()}/app/dataset/world_position.csv')
            elif data_type == 'age_data':
                return pd.read_excel(f'{os.getcwd()}/app/dataset/age_data.xlsx')
            elif data_type == 'gender_data':
                return pd.read_excel(f'{os.getcwd()}/app/dataset/gender_data.xlsx')
            elif data_type == 'global_data':
                return pd.read_excel(f'{os.getcwd()}/app/dataset/world_data.xlsx')
            elif data_type == 'korea_data':
                return pd.read_excel(f'{os.getcwd()}/app/dataset/korea_data.xlsx')

        except (Exception,):
            pass

    # ========================================================
    # 데이터베이스 입력 시 오류 방지를 위해
    # NaN값을 None(Null)으로 변환
    # ========================================================
    @staticmethod
    def convert_nan_to_none(value):
        if isinstance(value, float) and (math.isnan(value) or np.isnan(value)):
            return None

        return value

    # ========================================================
    # 테이블의 Row Count 계산
    # ========================================================
    @staticmethod
    def table_row_count(model):
        return SESSION.query(model).count()

    # ========================================================
    # 대량 데이터 삽입 기능 - 배치로 나눔
    # ========================================================
    @staticmethod
    def bulk_insert_data(data_list, once_limit=5000):
        try:
            for i in range(0, len(data_list), once_limit):
                batch = data_list[i:i + once_limit]

                SESSION.bulk_save_objects(batch)
                SESSION.commit()

        except Exception as e:
            SESSION.rollback()
            print(f'{e}')

        finally:
            SESSION.close()

    # ========================================================
    # 대량 데이터 삽입 기능 - pandas 이용
    # ========================================================
    @staticmethod
    def bulk_insert_data_pandas(model, data_frame):
        data_dicts = data_frame.to_dict(orient='records')
        model_instances = [model(**data) for data in data_dicts]

        try:
            SESSION.bulk_save_objects(model_instances)
            SESSION.commit()

        except Exception as e:
            print(f'{e} Error!')

    @staticmethod
    def select_one(model):
        work = select(model)
        return SESSION.scalars(work)
    
    @staticmethod
    def select_where_position(model, location):
        work = select(model).where(model.location.in_([location]))
        return SESSION.scalars(work)
    
    @staticmethod
    def select_where_nation(model, nation):
        work = select(model).where(model.nation.in_([nation]))
        return SESSION.scalars(work)
    
    @staticmethod
    def select_where_date(model, date):
        work = select(model).where(model.data_date.in_([date]))
        return SESSION.scalars(work)
    


    @staticmethod
    def data_push_list(data, is_global):
        new_list = []
        for data_one in data:

            if is_global:
                temp_list = {
                    'nation': data_one.nation,
                    'total_cases': data_one.total_cases,
                    'active_cases': data_one.active_cases,
                    'death_cases': data_one.death_cases,
                    're_rate': data_one.re_rate,
                    're_cases': data_one.re_cases
                }

            else:
                temp_list = {
                    'total_cases': data_one.total_cases,
                    'active_cases': data_one.active_cases,
                    'death_cases': data_one.death_cases,
                    're_rate': data_one.re_rate,
                    're_cases': data_one.re_cases
                }

            new_list.append(temp_list)
        return new_list
    


    @staticmethod
    def get_model_page(model, date, page, per_page):
        offset = (page - 1) * per_page
        users = SESSION.query(model).filter(getattr(model, 'data_date') == date).limit(per_page).offset(offset).all()
        return users

    
    # 딕셔너리를 포함하는 리스트를 입력받아 정수 세자리 마라 콤마를 찍어 str 형태로 변환하는 함수
    @staticmethod
    def add_comma_to_list(list_name): 
        for idx in range(len(list_name)):
            list_name[idx]['total_cases'] = Common.add_comma(int(list_name[idx]['total_cases']))
            list_name[idx]['active_cases'] = Common.add_comma(int(list_name[idx]['active_cases']))
            list_name[idx]['death_cases'] = Common.add_comma(int(list_name[idx]['death_cases']))
            list_name[idx]['re_cases'] = Common.add_comma(int(list_name[idx]['re_cases']))
        return list_name
    
    @staticmethod
    def add_comma(num):
        if num < 1000:
            comma_num = str(num)[0]+","+str(num)[-3:]
        elif (num > 1000) & (num < 1000000):
            comma_num = str(num)[-6:-3]+","+str(num)[-3:]
        elif (num > 1000000) & (num < 1000000000):
            comma_num = str(num)[-9:-6]+","+str(num)[-6:-3]+","+str(num)[-3:]
        return comma_num



    # 영어로 된 한국의 도시명을 한국어로 변환해주는 함수
    def mapping_city_name(city_name):
        dict_city_name = {
            "Busan":"부산광역시",
            "Chungcheongbuk":"충청북도",
            "Chungcheongnam":"충청남도",
            "Daegu":"대구광역시",
            "Daejeon":"대전광역시",
            "Gangwon":"강원특별자치도",
            "Gwangju":"광주광역시",
            "Gyeonggi":"경기도",
            "Gyeongsangbuk":"경상북도",
            "Gyeongsangnam":"경상남도",
            "Incheon":"인천광역시",
            "Jeju":"제주특별자치도",
            "Jeollabuk":"전라북도",
            "Jeollanam":"전라남도",
            "Sejong":"세종특별자치시",
            "Seoul":"서울특별시",
            "Ulsan":"울산광역시",
        }

        return dict_city_name[city_name]