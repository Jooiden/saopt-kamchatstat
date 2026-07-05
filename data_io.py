import sqlite3
import os

DB_NAME = "kamstat.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

# --- АВТОРИЗАЦИЯ И ПОЛЬЗОВАТЕЛИ ---

def login_user(login, password):
    conn = get_connection()
    cursor = conn.cursor()
    # Соединяем таблицы для получения ФИО
    cursor.execute("""
        SELECT u.id, e.fio, u.role_id 
        FROM users u
        JOIN employees e ON u.employee_id = e.id
        WHERE u.login=? AND u.password=?
    """, (login, password))
    user = cursor.fetchone()
    conn.close()
    return user

def login_exists(login):
    """Проверяет, занят ли логин при регистрации нового пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE login = ?", (login,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT u.id, e.fio, u.login, u.password, u.role_id, d.name 
        FROM users u
        JOIN employees e ON u.employee_id = e.id
        LEFT JOIN departments d ON u.department_id = d.id
        ORDER BY e.fio ASC
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def add_new_user(fio, login, password, role_id, dept_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Создаем запись сотрудника
        cursor.execute("INSERT INTO employees (fio, dept_id) VALUES (?, ?)", (fio, dept_id))
        emp_id = cursor.lastrowid
        # 2. Создаем учетную запись привязанную к нему
        cursor.execute("""
            INSERT INTO users (employee_id, login, password, role_id, department_id) 
            VALUES (?, ?, ?, ?, ?)
        """, (emp_id, login, password, role_id, dept_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при добавлении: {e}")
        return False
    finally:
        conn.close()

def update_user_password(user_id, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
    conn.commit()
    conn.close()

def delete_user_completely(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    # Узнаем ID сотрудника перед удалением пользователя
    cursor.execute("SELECT employee_id FROM users WHERE id=?", (user_id,))
    res = cursor.fetchone()
    if res:
        emp_id = res[0]
        cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

#ТЕСТЫ И РЕЗУЛЬТАТЫ

def get_all_tests():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, variants_count, mu, sigma FROM tests")
        return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка получения списка тестов: {e}")
        return []
    finally:
        conn.close()

def get_questions_for_test(test_id):
    conn = get_connection()
    #id, чтобы передать его в функцию выше!
    res = conn.execute("""
        SELECT question_text, is_direct, id 
        FROM questions 
        WHERE test_id = ? 
        ORDER BY id ASC
    """, (test_id,)).fetchall()
    conn.close()
    return res

def save_result(user_id, test_id, score):
    conn = get_connection()
    cursor = conn.cursor()
    # Сохраняем балл
    cursor.execute("INSERT INTO results (user_id, test_id, score, date) VALUES (?, ?, ?, datetime('now'))", 
                   (user_id, test_id, score))
    # Обновляем статус назначения
    cursor.execute("UPDATE assignments SET status=1 WHERE user_id=? AND test_id=?", (user_id, test_id))
    conn.commit()
    conn.close()

def get_filtered_results(query=None, d_from=None, d_to=None):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        SELECT e.fio, t.name, r.score, r.date, u.id, t.id 
        FROM results r 
        JOIN users u ON r.user_id = u.id 
        JOIN employees e ON u.employee_id = e.id
        JOIN tests t ON r.test_id = t.id 
        WHERE 1=1
    """
    params = []
    if query:
        sql += " AND e.fio LIKE ?"
        params.append(f"%{query}%")
    if d_from:
        sql += " AND r.date >= ?"
        params.append(d_from)
    if d_to:
        sql += " AND r.date <= ?"
        params.append(d_to)
    
    sql += " ORDER BY r.date DESC"
    cursor.execute(sql, params)
    data = cursor.fetchall()
    conn.close()
    return data

def get_my_assignments(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, t.name 
        FROM tests t
        JOIN assignments a ON t.id = a.test_id
        WHERE a.user_id = ? AND a.status = 0
    """, (user_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def get_departments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM departments") 
    data = [row[0] for row in cursor.fetchall()]
    conn.close()
    return data if data else ["Общий отдел"]

def assign_test_to_user(user_id, test_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM assignments WHERE user_id=? AND test_id=? AND status=0", (user_id, test_id))
        if cursor.fetchone():
            return True
        cursor.execute("INSERT INTO assignments (user_id, test_id) VALUES (?, ?)", (user_id, test_id))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_test_settings(test_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, variants_count, mu, sigma FROM tests WHERE id=?", (test_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def get_test_info(test_id):
    data = get_test_settings(test_id)
    if data:
        return {'name': data[0], 'mu': data[2], 'sigma': data[3]}
    return {'name': 'Unknown', 'mu': 0, 'sigma': 1}

def get_variants_for_question(q_id):
    """Получает список вариантов ответов для конкретного вопроса из БД"""
    conn = get_connection()
    try:
        # Мы берем текст варианта и его балл
        # Сортируем по id, чтобы порядок ответов был как в базе
        res = conn.execute("""
            SELECT variant_text, score_value 
            FROM question_variants 
            WHERE question_id = ? 
            ORDER BY id ASC
        """, (q_id,)).fetchall()
        return res
    except Exception as e:
        print(f"Ошибка при получении вариантов: {e}")
        return []
    finally:
        conn.close()