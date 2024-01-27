from sqlalchemy import create_engine, MetaData, Table, select, text
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
donations_table = metadata.tables['donations']
sponsors_table = metadata.tables['sponsors']
departments_table = metadata.tables['departments']

# Ваш SQL-запит
selected_month = 1  # Замініть на конкретне значення місяця
select_query = (
    select([
        departments_table.c['name'].label('department'),
        sponsors_table.c['name'].label('sponsor'),
        donations_table.c['amount'].label('donation_amount'),
        donations_table.c['date'].label('donation_date')
    ])
    .select_from(
        donations_table
        .join(sponsors_table, donations_table.c['sponsor_id'] == sponsors_table.c['id'])
        .join(departments_table, donations_table.c['department_id'] == departments_table.c['id'])
    )
    .where(text(f"EXTRACT(MONTH FROM donations.date) = {selected_month}"))
)

try:
    with engine.connect() as connection:
        results = connection.execute(select_query).fetchall()

        print(f"Пожертвування за місяць {selected_month}:")
        for row in results:
            print(f"Відділення: {row['department']}, Спонсор: {row['sponsor']}, "
                  f"Сума пожертвування: {row['donation_amount']}, Дата пожертвування: {row['donation_date']}")

except Exception as e:
    print(f"Помилка підключення до бази даних: {e}")
