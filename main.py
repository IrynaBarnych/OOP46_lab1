from sqlalchemy import create_engine, MetaData, Table, Column, insert, update, delete
from sqlalchemy.sql import select
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

def display_all_tables():
    print("Назви усіх таблиць:")
    for table_name in metadata.tables.keys():
        print(table_name)

def display_columns(table_name):
    if table_name in metadata.tables:
        table = metadata.tables[table_name]
        print(f"Назви стовпців для таблиці {table_name}:")
        for column in table.columns:
            print(column.name)
    else:
        print("Такої таблиці не існує.")

def display_columns_with_types(table_name):
    if table_name in metadata.tables:
        table = metadata.tables[table_name]
        print(f"Назви стовпців та їх типи для таблиці {table_name}:")
        for column in table.columns:
            print(f"{column.name}: {column.type}")
    else:
        print("Такої таблиці не існує.")

def display_relationships():
    print("Зв’язки між таблицями:")
    for table_name, table in metadata.tables.items():
        for foreign_key in table.foreign_keys:
            print(f"{table_name}.{foreign_key.parent.name} -> {foreign_key.column.table.name}.{foreign_key.column.name}")

def create_table(table_name, column_definitions):
    # column_definitions - список з описом стовпців (наприклад, [('column1', 'INT'), ('column2', 'VARCHAR(255)')])
    columns = [Column(name, eval(column_type)) for name, column_type in column_definitions]
    Table(table_name, metadata, *columns).create(engine)

def delete_table(table_name):
    if table_name in metadata.tables:
        table = metadata.tables[table_name]
        table.drop(engine)
        print(f"Таблицю {table_name} видалено.")
    else:
        print("Такої таблиці не існує.")

def add_column(table_name, column_name, column_type):
    if table_name in metadata.tables:
        table = metadata.tables[table_name]
        column = Column(column_name, eval(column_type))
        column.create(table, bind=engine)
        print(f"Стовпець {column_name} додано до таблиці {table_name}.")
    else:
        print("Такої таблиці не існує.")

def update_column(table_name, column_name, new_column_type):
    if table_name in metadata.tables:
        table = metadata.tables[table_name]
        if column_name in table.columns:
            table.c[column_name].alter(type=eval(new_column_type))
            print(f"Стовпець {column_name} оновлено у таблиці {table_name}.")
        else:
            print(f"Стовпець {column_name} не існує у таблиці {table_name}.")
    else:
        print("Такої таблиці не існує.")

def delete_column(table_name, column_name):
    if table_name in metadata.tables:
        table = metadata.tables[table_name]
        if column_name in table.columns:
            column = table.c[column_name]
            column.drop(engine)
            print(f"Стовпець {column_name} видалено з таблиці {table_name}.")
        else:
            print(f"Стовпець {column_name} не існує у таблиці {table_name}.")
    else:
        print("Такої таблиці не існує.")

while True:
    print("Оберіть опцію:")
    print("1. Відобразити назви усіх таблиць")
    print("2. Відобразити назви стовпців певної таблиці")
    print("3. Відобразити назви стовпців та їх типів для певної таблиці")
    print("4. Відобразити зв’язки між таблицями")
    print("5. Створити таблиці")
    print("6. Видалити таблиці")
    print("7. Додати стовпці")
    print("8. Оновити стовпці")
    print("9. Видалити стовпці")
    print("0. Вийти")

    choice = input("Введіть номер опції: ")

    if choice == "1":
        display_all_tables()
    elif choice == "2":
        table_name = input("Введіть назву таблиці: ")
        display_columns(table_name)
    elif choice == "3":
        table_name = input("Введіть назву таблиці: ")
        display_columns_with_types(table_name)
    elif choice == "4":
        display_relationships()
    elif choice == "5":
        table_name = input("Введіть назву таблиці: ")
        column_definitions = []
        while True:
            column_name = input("Введіть назву стовпця (або 0, щоб завершити): ")
            if column_name == '0':
                break
            column_type = input("Введіть тип стовпця: ")
            column_definitions.append((column_name, column_type))
        create_table(table_name, column_definitions)
    elif choice == "6":
        table_name = input("Введіть назву таблиці: ")
        delete_table(table_name)
    elif choice == "7":
        table_name = input("Введіть назву таблиці: ")
        column_name = input("Введіть назву стовпця: ")
        column_type = input("Введіть тип стовпця: ")
        add_column(table_name, column_name, column_type)
    elif choice == "8":
        table_name = input("Введіть назву таблиці: ")
        column_name = input("Введіть назву стовпця: ")
        new_column_type = input("Введіть новий тип стовпця: ")
        update_column(table_name, column_name, new_column_type)
    elif choice == "9":
        table_name = input("Введіть назву таблиці: ")
        column_name = input("Введіть назву стовпця: ")
        delete_column(table_name, column_name)
    elif choice == "0":
        break
    else:
        print("Невірний вибір. Будь ласка, оберіть знову.")

