import time
import psycopg2

class DatabaseService:
    def __init__(self, host, port, dbname, user, password, retries=5, delay=3):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password

        self.conn = None
        self._wait_for_db(retries, delay)
        self._create_table_if_not_exists()  # <-- ВАЖНО! Этот метод должен существовать

    def _wait_for_db(self, retries, delay):
        """Ждём, пока PostgreSQL поднимется"""
        for attempt in range(retries):
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password
                )
                print("✅ PostgreSQL доступен!")
                return
            except psycopg2.OperationalError as e:
                print(f"⏳ Ожидание PostgreSQL... Попытка {attempt + 1}/{retries}")
                time.sleep(delay)
        raise Exception("❌ Не удалось подключиться к PostgreSQL!")

    def _create_table_if_not_exists(self):
        """Создаёт таблицу, если её нет"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP NOT NULL,
            parameter_name VARCHAR(255) NOT NULL,
            value DOUBLE PRECISION NOT NULL,
            ts_now TIMESTAMP DEFAULT NOW()
        );
        """
        with self.conn.cursor() as cursor:
            cursor.execute(create_table_sql)
            self.conn.commit()
        print("✅ Таблица проверена/создана!")

    def insert_record(self, created_at, parameter_name, value, ts_now):
        """Вставляет запись в БД, корректируя формат времени"""
        created_at = created_at.split('.')[0]  # Оставляем только до секунд
        insert_sql = """
           INSERT INTO sensor_readings (created_at, parameter_name, value, ts_now)
           VALUES (TO_TIMESTAMP(%s, 'YYYY-MM-DD"T"HH24:MI:SS'), %s, %s, NOW());
           """
        with self.conn.cursor() as cursor:
            cursor.execute(insert_sql, (created_at, parameter_name, value))
            self.conn.commit()
        print("✅ Данные успешно вставлены в БД")
