from sqlalchemy import Column, Integer, String, Table, ForeignKey, PickleType
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

image_tags = Table(
    "image_tags",
    Base.metadata,
    Column("image_id", ForeignKey("images.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    path = Column(String, unique=True, nullable=False)
    embedding = Column(PickleType)

    tags = relationship("Tag", secondary=image_tags, back_populates="images")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    images = relationship("Image", secondary=image_tags, back_populates="tags")
