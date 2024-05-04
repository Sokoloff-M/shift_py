from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from database import get_db

# Создаем экземпляр приложения FastAPI
app = FastAPI()

# Создаем базовый класс для объявления моделей SQLAlchemy
Base = declarative_base()

# Определяем модель Employee для таблицы employees в базе данных
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    salary = Column(Integer)

# Создаем соединение с базой данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Создаем фабрику сессий для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для создания нового сотрудника
def create_employee(db: Session, name: str, salary: int):
    db_employee = Employee(name=name, salary=salary)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Функция для получения списка всех сотрудников
def get_employees(db: Session):
    return db.query(Employee).all()

# Маршрут для создания нового сотрудника
@app.post("/employees/")
async def create_employee_route(name: str, salary: int, db: Session = Depends(get_db)):
    employee = create_employee(db, name, salary)
    return employee

# Маршрут для получения списка всех сотрудников
@app.get("/employees/")
async def get_employees_route(db: Session = Depends(get_db)):
    employees = get_employees(db)
    return employees 
