from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

Base = declarative_base()

class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    salary = Column(Integer)
    surname = Column(String)
    specializations = relationship('Specialization', secondary='doctors_specializations')

class Specialization(Base):
    __tablename__ = 'specializations'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class DoctorsSpecializations(Base):
    __tablename__ = 'doctors_specializations'
    doctor_id = Column(Integer, ForeignKey('doctors.id'), primary_key=True)
    specialization_id = Column(Integer, ForeignKey('specializations.id'), primary_key=True)

# Підключення до бази даних
engine = create_engine('sqlite:///hospital.db')  # Використовуйте свій рядок підключення

# Створення таблиць у базі даних
Base.metadata.create_all(engine)

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

# Запит для виведення прізвищ лікарів та їх спеціалізацій
doctors_specializations = session.query(Doctor.surname, Specialization.name).join(Doctor.specializations).all()

# Виведення результатів
for doctor_surname, specialization_name in doctors_specializations:
    print(f"{doctor_surname}: {specialization_name}")

# Закриття сесії
session.close()

