from app.database import CONNECTION
from app.modules.positions import Positions

# insert 함수
def insert():
    p = Positions()
    
    insert_data = p.get_dataset_positions('korea')
    p.insert_table_korea_position(insert_data)


# table_name: 가져올 데이터베이스의 테이블명
# date: 가져올 데이터의 날짜
def select(table_name, date):
    try:
        conn = CONNECTION
        
        cursor = conn.cursor()
        sql = f"SELECT * FROM {table_name} WHERE address_lev1 = '경기도'"
        cursor.execute(sql)

        data = cursor.fetchall()
        return data
    
    except ConnectionError:
        print("에러 발생")