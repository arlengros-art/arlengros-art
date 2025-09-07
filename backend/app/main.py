from typing import List

from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session

from . import embeddings, models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/gallery")
def get_gallery(q: str | None = Query(default=None), db: Session = Depends(get_db)):
    images: List[models.Image] = db.query(models.Image).all()
    if q:
        query_emb = embeddings.text_embedding(q)
        images.sort(
            key=lambda im: cosine_similarity(query_emb, im.embedding),
            reverse=True,
        )
    return [
        {
            "id": im.id,
            "path": im.path,
            "tags": [t.name for t in im.tags],
        }
        for im in images
    ]

def cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    import math

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
