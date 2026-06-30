
from src.db_manager import DBManager

from db import create_tables, get_connection, fill_tables

conn = get_connection()

create_tables(conn)

fill_tables(conn)

db = DBManager(conn)

print("Все самолеты:")
print(db.get_all_aeroplanes())

print("Средняя скорость:")
print(db.get_avg_speed())

print("Количество самолетов по странам:")
print(db.get_countries_and_aeroplanes_count())

print("Самолеты быстрее средней:")
print(db.get_aeroplanes_with_higher_speed())

print("Поиск по позывному ACA:")
print(db.get_aeroplanes_with_keyword("ACA"))