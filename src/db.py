import os

import psycopg2
from dotenv import load_dotenv

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
