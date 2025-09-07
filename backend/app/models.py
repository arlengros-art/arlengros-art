from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Image(Base):
    """Simple image model."""
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    # New field indicating whether the image has passed moderation
    is_approved = Column(Boolean, default=False, nullable=False)
