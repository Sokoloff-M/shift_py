from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from pydantic import BaseModel
from .database import SessionLocal, get_db
from .models import User, UserCreate

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для хеширования пароля
def hash_password(password: str):
    return pwd_context.hash(password)

# Функция для проверки соответствия хешированного пароля и пароля введенного пользователем
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Маршрут для аутентификации пользователя
@router.post("/login/")
async def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return {"message": "Login successful"}

# Маршрут для создания нового пользователя
@router.post("/register/")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(username=user.username, password=hash_password(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User created successfully"}
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
# Маршрут для аутентификации пользователя по токену