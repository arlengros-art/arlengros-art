from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Gallery(Base):
    """Simple gallery item model."""

    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True)
    prompt = Column(String, nullable=False)
    style = Column(String, nullable=True)

    # explicit indexes to speed up text search and style filtering
    __table_args__ = (
        Index("ix_gallery_prompt", "prompt"),
        Index("ix_gallery_style", "style"),
    )
