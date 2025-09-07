from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

from . import models

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProfileUpdate(BaseModel):
    username: str
    bio: str | None = None
    avatar_url: str | None = None


@app.post("/profile")
def update_profile(profile: ProfileUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username=profile.username).first()
    if not user:
        user = models.User(username=profile.username)
        db.add(user)
    user.bio = profile.bio or ""
    user.avatar_url = profile.avatar_url or ""
    db.commit()
    db.refresh(user)
    likes_count = db.query(models.Like).filter_by(user_id=user.id).count()
    return {
        "username": user.username,
        "bio": user.bio,
        "avatar_url": user.avatar_url,
        "likes": likes_count,
    }


@app.get("/profile/{username}")
def get_profile(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    likes_count = db.query(models.Like).filter_by(user_id=user.id).count()
    return {
        "username": user.username,
        "bio": user.bio,
        "avatar_url": user.avatar_url,
        "likes": likes_count,
    }


@app.post("/like/{image_id}")
def like_image(image_id: int, username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    image = db.query(models.Image).filter_by(id=image_id).first()
    if not image:
        image = models.Image(id=image_id, url=f"/images/{image_id}.jpg")
        db.add(image)
        db.commit()
        db.refresh(image)
    existing = db.query(models.Like).filter_by(user_id=user.id, image_id=image.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already liked")
    like = models.Like(user_id=user.id, image_id=image.id)
    db.add(like)
    db.commit()
    count = db.query(models.Like).filter_by(image_id=image.id).count()
    return {"image_id": image.id, "likes": count}
