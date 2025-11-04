from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/all", response_model=list[UserResponse])
def list_all_users(db: Session = Depends(get_db)):

    users = db.query(User).all()
    return users
