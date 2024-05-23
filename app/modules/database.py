from database import CONNECTION

def select(table_name, date):
    try:
        conn = CONNECTION
        
        cursor = conn.cursor()
        sql = f"SELECT * FROM {table_name} WHERE date = {date}"
        cursor.execute(sql)

        data = cursor.fetchall()
        return data
    
    except ConnectionError:
        print("에러 발생")

    finally:
        if conn:
            conn.close()