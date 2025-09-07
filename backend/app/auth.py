from datetime import datetime, timedelta
import hashlib
from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_token(username: str):
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = hashlib.sha256(user.password.encode()).hexdigest()
    db_user = User(username=user.username, password_hash=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = create_token(db_user.username)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    hashed = hashlib.sha256(user.password.encode()).hexdigest()
    if hashed != db_user.password_hash:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_token(db_user.username)
    return {"access_token": token, "token_type": "bearer"}
