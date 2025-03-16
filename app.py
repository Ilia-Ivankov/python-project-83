import os
import psycopg2

def check_db_connection():
    """
    Проверяет соединение с базой данных PostgreSQL, используя DATABASE_URL из переменных окружения.
    Выводит сообщение об успехе или ошибке подключения.
    """
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("Ошибка: Переменная окружения DATABASE_URL не найдена.")
        return False

    try:
        conn = psycopg2.connect(db_url)
        conn.close() # Просто проверяем соединение, закрываем сразу
        print("Успешно: Соединение с базой данных установлено!")
        return True
    except psycopg2.Error as e:
        print(f"Ошибка: Не удалось подключиться к базе данных. {e}")
        return False

if __name__ == "__main__":
    check_db_connection()
