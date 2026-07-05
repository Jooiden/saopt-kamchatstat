import sqlite3
from data_io import get_connection

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # объединение таблицы users и employees по полю employee_id, 
        # достаем ФИО 
        query = """
            SELECT u.id, e.fio, u.role_id, u.password 
            FROM users u
            JOIN employees e ON u.employee_id = e.id
            WHERE u.login = ?
        """
        cursor.execute(query, (username,))
        user_record = cursor.fetchone()
    except Exception as e:
        print(f"Ошибка БД: {e}")
        return None
    finally:
        conn.close()

    if user_record:
        user_id, fio, role_id, db_password = user_record
        
        # Сверка пароля
        if str(password) == str(db_password):
            return (user_id, fio, role_id)
        else:
            print(f"Неверный пароль для {username}")
            
    return None