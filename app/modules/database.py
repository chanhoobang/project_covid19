from database import CONNECTION


def select(table_name):
    try:
        conn = CONNECTION
        
        cursor = conn.cursor()
        sql = f"select * from {table_name}"
        cursor.execute(sql)

        data = cursor.fetchall()
        return data
    
    except ConnectionError:
        print("에러 발생")

    finally:
        if conn:
            conn.close()