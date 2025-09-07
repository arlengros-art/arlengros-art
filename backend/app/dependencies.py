from datetime import datetime

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import ApiKey, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_api_key(
    api_key: str = Security(api_key_header), db: Session = Depends(get_db)
) -> ApiKey:
    """Dependency that ensures the provided API key exists."""
    if not api_key:
        raise HTTPException(status_code=403, detail="API key required")

    key_obj = db.query(ApiKey).filter(ApiKey.key == api_key).first()
    if not key_obj:
        raise HTTPException(status_code=403, detail="Invalid API key")

    key_obj.last_used = datetime.utcnow()
    db.commit()
    return key_obj
