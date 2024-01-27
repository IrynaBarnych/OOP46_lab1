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

# Визначення таблиць
doctors_table = metadata.tables['doctors']
vacations_table = metadata.tables['vacations']

# Ваш залишений код для виконання запиту
select_query = select([doctors_table.c['name'], doctors_table.c['salary']]).where(
    doctors_table.c['id'].notin_(
        select([vacations_table.c['doctor_id']])
    )
)

try:
    with engine.connect() as connection:
        results = connection.execute(select_query).fetchall()

        print("Прізвища та зарплати лікарів, які не перебувають у відпустці:")
        for row in results:
            print(f"Ім'я: {row['name']}, Зарплата: {row['salary']}")

except Exception as e:
    print(f"Помилка підключення до бази даних: {e}")

