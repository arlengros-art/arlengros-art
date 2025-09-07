from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .dependencies import get_db, require_admin
from .models import Image

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/images", response_model=List[dict])
async def get_pending_images(
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    """Return all images waiting for moderation"""
    images = db.query(Image).filter(Image.is_approved.is_(False)).all()
    return [{"id": i.id, "url": i.url} for i in images]

@router.post("/image/{image_id}/approve")
async def approve_image(
    image_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    image = db.get(Image, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    image.is_approved = True
    db.commit()
    return {"status": "approved"}

@router.delete("/image/{image_id}")
async def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    image = db.get(Image, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(image)
    db.commit()
    return {"status": "deleted"}
