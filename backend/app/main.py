from fastapi import FastAPI

from . import models
from .admin import router as admin_router
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(admin_router)
