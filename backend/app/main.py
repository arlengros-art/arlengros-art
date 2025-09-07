from typing import List, Optional

from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base, Gallery

DATABASE_URL = "sqlite:///./gallery.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/gallery", response_model=List[dict])
def get_gallery(
    q: Optional[str] = None,
    style: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Return gallery items with optional search and style filter."""
    query = db.query(Gallery)
    if q:
        query = query.filter(Gallery.prompt.contains(q))
    if style:
        query = query.filter(Gallery.style == style)
    items = query.all()
    return [
        {"id": item.id, "prompt": item.prompt, "style": item.style}
        for item in items
    ]
