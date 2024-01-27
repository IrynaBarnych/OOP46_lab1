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
departments_table = metadata.tables['departments']
sponsors_table = metadata.tables['sponsors']
sponsorships_table = metadata.tables['sponsorships']

# Ваш SQL-запит
company_name = 'Company XYZ'  # Замініть на конкретне ім'я компанії
select_query = (
    select([
        departments_table.c['name'].label('department')
    ])
    .distinct()
    .select_from(
        departments_table
        .join(sponsorships_table, departments_table.c['id'] == sponsorships_table.c['department_id'])
        .join(sponsors_table, sponsorships_table.c['sponsor_id'] == sponsors_table.c['id'])
    )
    .where(sponsors_table.c['name'] == company_name)
)

try:
    with engine.connect() as connection:
        results = connection.execute(select_query).fetchall()

        print(f"Назви відділень, які спонсоруються компанією {company_name}:")
        for row in results:
            print(f"Відділення: {row['department']}")

except Exception as e:
    print(f"Помилка підключення до бази даних: {e}")

