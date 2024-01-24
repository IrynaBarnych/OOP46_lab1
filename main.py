from sqlalchemy import create_engine, MetaData, Table, insert, update, delete
from sqlalchemy.sql import select
import psycopg2
import json

# Зчитування конфігураційних даних з файлу
with open('config.json') as f:
    config = json.load(f)

# Отримання логіну та паролю з об'єкта конфігурації
db_user = config['user']
db_password = config['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/Hospital'
engine = create_engine(db_url)
# з'єднання з БД
conn = engine.connect()
metadata = MetaData()
# завантаження таблиць
# автоматичне завантаження
metadata.reflect(bind=engine)
# або одна табличка
#departments = Table('departments', metadata, autoload=True, autoload_with=engine)

def insert_row(table: metadata):
    columns = table.columns.keys()

    values = {}
    for columns in columns:
        value = input(f"Введіть значення для колонки {columns}")
        values[columns] = value
    query = insert(table).values(values)
    conn.execute(query)
    conn.commit()

    print("Рядок успішно додано!")

def update_rows(table):
    columns = table.columns.keys()
    print("Доступні колонки для оновлення: ")
    for idx, column in enumerate(columns, start=1):
        print(f"{idx}.{column}")
    selected_column_idx = int(input("ВВедіть номер колонки для оновлення: "))

    if 1 <= selected_column_idx <= len(columns):
        condition_column = columns[selected_column_idx - 1]
    else:
        print("невірний номер колонки!")

    condition_value = input("ВВедіть значення для умови, {condition_column}: ")
    new_values = {}
    for column in columns:
        value = input(f"ВВедіть значення для колонки {column}: ")
        new_values[column] = value

    confirm_update = input("Оновити усі рядки? у/п? ")
    if confirm_update.lower() == 'y':
        query = update(table).where(getattr(table.c, condition_column) == condition_value).values(new_values)
        conn.execute(query)
        conn.commit()


def delete_rows(table):
    columns = table.columns.keys()
    print("Доступні колонки для видалення: ")
    for idx, column in enumerate(columns, start=1):
        print(f"{idx}.{column}")
    selected_column_idx = int(input("ВВедіть номер колонки для умови видалення: "))

    if 1 <= selected_column_idx <= len(columns):
        condition_column = columns[selected_column_idx - 1]
    else:
        print("невірний номер колонки! Видалення відмінено!")

    condition_value = input("ВВедіть значення для умови, {condition_column}: ")

    confirm_update = input("Видалити усі рядки з цієї таблиці? у/п? ")
    if confirm_update.lower() == 'y':
        query = delete(table).where(getattr(table.c, condition_column) == condition_value)
        conn.execute(query)
        conn.commit()

while True:
    print("Оберіть таблицю: ")
    for table_name in metadata.tables.keys():
        print(table_name)
    table_name = input("Введіть назву таблиці або 0, щоб вийти ")
    if table_name == '0':
        break
    # перевіримо, чи існує таблиця
    if table_name in metadata.tables:
        table = metadata.tables[table_name]
        print(f"Ви обрали таблицю {table_name}")

        print("1. Вставити рядки")
        print("2. Оновити рядки")
        print("3. Видалити рядки")
        print("0. Вийти")

        choice = input("Оберіть опцію: ")

        if choice == "1":
            insert_row(table)
        elif choice == "2":
            update_rows(table)
        elif choice == "3":
            delete_rows(table)
        elif choice == "0":
            break
        else:
            print("Невірний вибір. Будь ласка, оберіть знову.")
    else:
        print("Такої таблиці не існує. Будь ласка, введіть правильну назву.")
