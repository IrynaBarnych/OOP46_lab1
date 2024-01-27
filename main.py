from sqlalchemy import create_engine, MetaData, Table, select
import json

# Зчитування конфігураційних даних з файлу
with open('config.json') as f:
    config = json.load(f)

# Отримання логіну та паролю з об'єкта конфігурації
db_user = config['user']
db_password = config['password']

# Створення engine для підключення до бази даних
db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/Hospital'
engine = create_engine(db_url)

# З'єднання з БД
conn = engine.connect()

metadata = MetaData()

# Завантаження таблиць - автоматичне завантаження
metadata.reflect(bind=engine)

# Визначення таблиці
wards_table = metadata.tables['wards']

# Ваш SQL-запит
department_id = 1  # Замініть на конкретне значення
select_query = select([wards_table.c['name']]).where(
    wards_table.c['department_id'] == department_id
)

try:
    with engine.connect() as connection:
        results = connection.execute(select_query).fetchall()

        print(f"Назви палат у відділенні з ID {department_id}:")
        for row in results:
            print(row['name'])

except Exception as e:
    print(f"Помилка підключення до бази даних: {e}")

