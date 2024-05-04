from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Создаем экземпляр движка базы данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаем фабрику сессий для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)





def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()