import psycopg2

from api import get_planes_in_country
from db import get_connection

conn = get_connection()
cur = conn.cursor()


class DBManager:
    """
    Класс для работы с PostgreSQL.
    """
    def __init__(self, conn):
        """Инициализирует подключение к базе данных."""
        self.conn = conn

    def get_countries_and_aeroplanes_count(self):
        """

        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, COUNT(p.id)
                FROM countries c
                LEFT JOIN planes p ON c.id = p.country_id
                GROUP BY c.name
            """)
            return cur.fetchall()

    def get_all_aeroplanes(self):
        """
            Получает список всех самолетов из базы данных.
        :return:
            """
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM planes")
            return cur.fetchall()

    def get_avg_speed(self):
        """
            Получает среднюю скорость всех самолетов.
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(speed)
                FROM planes
                WHERE speed IS NOT NULL
            """)
            return cur.fetchone()[0]

    def get_aeroplanes_with_higher_speed(self):
        """
          Получает список самолетов, у которых скорость выше средней.
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM planes
                WHERE speed > (
                    SELECT AVG(speed)
                    FROM planes
                    WHERE speed IS NOT NULL
                )
            """)
            return cur.fetchall()

    def get_aeroplanes_with_keyword(self, keyword):
        """
            Получает список самолетов с ключевым словом в названии самолета.
        :param keyword:
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM planes
                WHERE callsign ILIKE %s
            """,
                (f"%{keyword}%",),
            )
            return cur.fetchall()


cur.close()
conn.close()
