from pathlib import Path
from uuid import uuid4
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from PIL import Image as PILImage, ImageDraw

from . import database, models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


MEDIA_DIR = Path(__file__).resolve().parent.parent / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/generate")
def generate(prompt: str, user_id: int = 1, db: Session = Depends(get_db)):
    """Generate an image for the given prompt and store it."""
    filename = f"{uuid4()}.png"
    filepath = MEDIA_DIR / filename

    image = PILImage.new("RGB", (512, 512), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), prompt, fill=(0, 0, 0))
    image.save(filepath)

    db_image = models.Image(user_id=user_id, path=filename, prompt=prompt, created_at=datetime.utcnow())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    return {"id": db_image.id, "path": f"/media/{filename}"}


@app.get("/gallery")
def gallery(user_id: int = 1, db: Session = Depends(get_db)):
    """Return list of generated images for the user."""
    images = (
        db.query(models.Image)
        .filter(models.Image.user_id == user_id)
        .order_by(models.Image.created_at.desc())
        .all()
    )
    return [
        {
            "id": img.id,
            "path": f"/media/{img.path}",
            "prompt": img.prompt,
            "created_at": img.created_at,
        }
        for img in images
    ]


@app.get("/media/{image_path}")
def get_image(image_path: str):
    filepath = MEDIA_DIR / image_path
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(filepath)
