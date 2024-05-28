from app.database import SESSION
from app.models.detail import GlobalData
from app.models.position import GlobalPosition
from app.modules.common import Common


# ===================================
# 해외 데이터 관련 기능 모음
# ===================================
class WorldModule:

    def __init__(self):
        self.session = SESSION

    # 해외 국가별 좌표 데이터 삽입
    @staticmethod
    def insert_global_position():
        try:
            data_set = Common.get_dataset('global_position')

            insert_data = []

            for idx in range(len(data_set)):
                data = {
                    'nation': data_set.values[idx][0],
                    'position_x': data_set.values[idx][2],
                    'position_y': data_set.values[idx][3]
                }
                insert_data.append(data)
            insert = [GlobalPosition(**item) for item in insert_data]

            SESSION.add_all(insert)
            SESSION.commit()

        except Exception as e:
            SESSION.rollback()
            print(e)

        finally:
            SESSION.close()

    # 일자별 해외 데이터 삽입
    @staticmethod
    def insert_global_date_data():
        data_set = Common.get_dataset('global_data')
        Common.bulk_insert_data_pandas(GlobalData, data_set)
