import os

import psycopg2
from dotenv import load_dotenv

from api import get_planes_in_country

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_connection():
    return psycopg2.connect(
        dbname="airplanes_db",
        user="postgres",
        password=DB_PASSWORD,
        host="localhost",
        port="5432",
    )

def create_tables(conn):
    """Создает таблицы базы данных countries и planes."""

    with conn.cursor() as cur:

        # очищаем старые таблицы, если они существуют
        cur.execute("""
            DROP TABLE IF EXISTS planes;
            DROP TABLE IF EXISTS countries;
        """)

        # создаем countries
        cur.execute("""
            CREATE TABLE countries (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL
            );
        """)

        # создаем planes
        cur.execute("""
            CREATE TABLE planes (
                id SERIAL PRIMARY KEY,
                icao24 VARCHAR(100) UNIQUE,
                callsign VARCHAR(100),
                speed FLOAT,
                country_id INTEGER REFERENCES countries(id)
            );
        """)



def fill_tables(conn):
    """Заполняет таблицы countries и planes."""

    countries = ["US", "France", "Germany", "Canada", "Russia"]

    for country in countries:

        cur = conn.cursor()

        cur.execute("INSERT INTO countries (name) VALUES (%s) RETURNING id", (country,))
        country_id = cur.fetchone()[0]

        conn.commit()

        data = get_planes_in_country(country)

        for plane in data["states"]:
            cur.execute(
                """
                INSERT INTO planes (icao24, callsign, speed, country_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (icao24)
                DO UPDATE SET
                    callsign = EXCLUDED.callsign,
                    speed = EXCLUDED.speed
                """,
                (plane[0], plane[1].strip() if plane[1] else None, plane[9], country_id),
            )

        conn.commit()