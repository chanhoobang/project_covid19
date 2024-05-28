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

    @staticmethod
    def get_table_record_count(model, date):
        return SESSION.query(model).filter(getattr(model, 'data_date') == date).count()

    @staticmethod
    def paginate(model, date, page, per_page=10):
        total = SESSION.query(model).filter(getattr(model, 'data_date') == date).count()
        items = SESSION.query(model).filter(getattr(model, 'data_date') == date).offset((page - 1) * per_page).limit(per_page).all()
        total_pages = math.ceil(total / per_page)

        return items, total_pages

    @staticmethod
    def get_columns(model):
        return [column.name for column in model.__table__.columns]
