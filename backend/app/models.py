from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Image(Base):
    """Database model storing generated images."""

    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    path = Column(String, nullable=False)
    prompt = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
