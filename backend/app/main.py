from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .models import ApiKey
from .dependencies import get_db

app = FastAPI()


class ApiKeyRequest(BaseModel):
    action: str


def get_current_user(authorization: str = Header(...)):
    if authorization != "Bearer secret":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"id": 1}


@app.post("/api-keys")
def api_keys_endpoint(
    payload: ApiKeyRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create or delete API keys for the current user."""
    if payload.action == "create":
        new_key = ApiKey.generate()
        key_obj = ApiKey(key=new_key, user_id=current_user["id"])
        db.add(key_obj)
        db.commit()
        db.refresh(key_obj)
        return {"key": new_key}

    if payload.action == "delete":
        db.query(ApiKey).filter(ApiKey.user_id == current_user["id"]).delete()
        db.commit()
        return {"deleted": True}

    raise HTTPException(status_code=400, detail="Invalid action")
