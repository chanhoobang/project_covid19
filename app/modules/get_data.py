import pymysql
import pymysql.cursors

from app.database import CONNECTION

# 데이터베이스에서 table_name에 해당하는 테이블 데이터를 받아오는 함수
def select(table_name):
    try:
        conn = CONNECTION

        cursor = conn.cursor()
        # 테이블명 입력 필요
        sql = f'select * from {table_name}'
        cursor.execute(sql)

        data_list = cursor.fetchall()
        return data_list
    
    except ConnectionError:
        print("에러 발생")
    finally:
        if conn:
            conn.close()
