from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import SessionLocal

class User:
    """Very small user representation"""
    def __init__(self, role: str):
        self.role = role

# This is a stub and should be replaced with real authentication
async def get_current_user() -> User:
    return User(role="admin")

# Dependency to get DB session
async def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ensure the current user has admin role
async def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return user
