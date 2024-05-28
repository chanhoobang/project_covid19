from app.database import SESSION
from app.models.detail import GenderData, AgeData, KoreaData
from app.models.position import KoreaPosition
from app.modules.common import Common


# ===================================
# 국내 데이터 관련 기능 모음
# ===================================
class KoreaModule:

    # 국내 시도별 좌표 데이터 삽입
    @staticmethod
    def insert_korea_position():
        try:
            data_set = Common.get_dataset('korea_position')

            insert_data = []

            for idx in range(len(data_set)):
                if Common.convert_nan_to_none(data_set.values[idx][1]) is None:
                    data = {
                        'location': data_set.values[idx][0],
                        'position_x': data_set.values[idx][3],
                        'position_y': data_set.values[idx][4]
                    }
                    insert_data.append(data)

            insert = [KoreaPosition(**item) for item in insert_data]

            SESSION.add_all(insert)
            SESSION.commit()

        except (Exception,):
            SESSION.rollback()

        finally:
            SESSION.close()

    # 성별 데이터(국내) 삽입
    @staticmethod
    def insert_korea_gender_data():
        data_set = Common.get_dataset('gender_data')
        Common.bulk_insert_data_pandas(GenderData, data_set)

    # 연령별 데이터(국내) 삽입
    @staticmethod
    def insert_korea_ages_data():
        data_set = Common.get_dataset('age_data')
        Common.bulk_insert_data_pandas(AgeData, data_set)

    # 전체 국내 데이터 삽입
    @staticmethod
    def insert_korea_data():
        data_set = Common.get_dataset('korea_data')
        Common.bulk_insert_data_pandas(KoreaData, data_set)
