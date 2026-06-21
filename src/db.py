import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="airplanes_db",
        user="postgres",
        password="derevo1576",
        host="localhost",
        port="5432"
    )