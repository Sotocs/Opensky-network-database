import psycopg2
from api import get_planes_in_country
from db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL

)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS planes (
    id SERIAL PRIMARY KEY,
    icao24 VARCHAR(100) UNIQUE,
    callsign VARCHAR(100),
    speed FLOAT,
    country_id INTEGER REFERENCES countries(id))""")
conn.commit()

countries = ["US", "France", "Germany", "Canada", "Russia"]
for country in countries:

    cur.execute(
        "INSERT INTO countries (name) VALUES (%s) RETURNING id",
        (country,)
    )
    country_id = cur.fetchone()[0]
    conn.commit()
    data = get_planes_in_country(country)
    if not data["states"]:
        continue

    for plane in data["states"]:
        icao24 = plane[0]
        callsign = plane[1].strip() if plane[1] else None
        speed = plane[9]

        cur.execute(
            """
    INSERT INTO planes (icao24, callsign, speed, country_id)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (icao24)
    DO UPDATE SET
        callsign = EXCLUDED.callsign,
        speed = EXCLUDED.speed,
        country_id = EXCLUDED.country_id
    """, (icao24, callsign, speed, country_id)
        )

    conn.commit()

cur.close()
conn.close()