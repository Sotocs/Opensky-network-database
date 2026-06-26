from api import get_planes_in_country
from db import get_connection
from db_manager import DBManager


def create_tables():
    """Создает таблицы countries и planes."""
    conn = get_connection()

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
