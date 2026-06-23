# OpenSky Network Database

Проект для получения информации о воздушных судах из API OpenSky Network и сохранения данных в базу данных PostgreSQL.

## Описание проекта

Приложение получает данные о самолетах, находящихся в воздушном пространстве выбранных стран, используя API OpenSky Network и Nominatim OpenStreetMap.

Собранные данные сохраняются в PostgreSQL и могут быть проанализированы с помощью класса `DBManager`.

## Используемые технологии

- Python 3.12+
- PostgreSQL
- psycopg2
- requests
- Poetry

## Функциональность

### Получение данных

- Получение координат страны через Nominatim API.
- Получение списка самолетов в воздушном пространстве страны через OpenSky API.
- Загрузка данных в PostgreSQL.

### Работа с базой данных

Класс `DBManager` предоставляет следующие методы:

| Метод | Описание |
|---------|---------|
| `get_countries_and_aeroplanes_count()` | Получает список стран и количество самолетов в каждой стране |
| `get_all_aeroplanes()` | Получает список всех самолетов |
| `get_avg_speed()` | Получает среднюю скорость самолетов |
| `get_aeroplanes_with_higher_speed()` | Получает самолеты со скоростью выше средней |
| `get_aeroplanes_with_keyword(keyword)` | Выполняет поиск самолетов по позывному |

---

## Структура проекта

```text
.
├── src/
│   ├── api.py
│   ├── db.py
│   ├── db_manager.py
│   ├── config.py
│   └── main.py
│
├── .env.example
├── README.md
├── requirements.txt
├── poetry.lock
├── poetry.toml
└── pyproject.toml
```

## Структура базы данных

### Таблица countries

| Поле | Тип |
|--------|--------|
| id | SERIAL PRIMARY KEY |
| name | VARCHAR(100) UNIQUE NOT NULL |

### Таблица planes

| Поле | Тип |
|--------|--------|
| id | SERIAL PRIMARY KEY |
| icao24 | VARCHAR(100) UNIQUE |
| callsign | VARCHAR(100) |
| speed | FLOAT |
| country_id | INTEGER REFERENCES countries(id) |

---

## Установка

### Клонирование репозитория

```bash
git clone <repository_url>
cd opensky-network-database
```

### Создание виртуального окружения

С использованием Poetry:

```bash
poetry install
```

или через pip:

```bash
pip install -r requirements.txt
```

---

## Настройка PostgreSQL

Создайте базу данных:

```sql
CREATE DATABASE airplanes_db;
```

Создайте таблицы:

```sql
CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE planes (
    id SERIAL PRIMARY KEY,
    icao24 VARCHAR(100) UNIQUE,
    callsign VARCHAR(100),
    speed FLOAT,
    country_id INTEGER REFERENCES countries(id)
);
```

---

## Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`.

Пример:

```env
DB_NAME=airplanes_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

## Запуск проекта

```bash
python src/main.py
```

После запуска приложение:

1. Получает координаты выбранных стран.
2. Загружает данные о самолетах через OpenSky API.
3. Сохраняет данные в PostgreSQL.
4. Обновляет существующие записи при повторной загрузке.

---

## Пример использования DBManager

```python
from db import get_connection
from db_manager import DBManager

conn = get_connection()

db = DBManager(conn)

print(db.get_all_aeroplanes())
print(db.get_avg_speed())
print(db.get_countries_and_aeroplanes_count())
print(db.get_aeroplanes_with_keyword("ACA"))
```

---

## Используемые API

### OpenSky Network API

Используется для получения информации о воздушных судах.

Документация:

https://openskynetwork.github.io/opensky-api/rest.html

### Nominatim API

Используется для получения географических координат стран.

Документация:

https://nominatim.org/release-docs/latest/api/Overview/

---

## Автор

Проект выполнен в рамках курсовой работы по работе с API и PostgreSQL.