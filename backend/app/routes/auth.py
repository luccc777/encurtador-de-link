from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud import user_crud
from app.schemas.user_schema import UserCreate, UserResponse
from app.schemas.auth_schema import Token, LoginRequest
from app.utils.jwt_handler import create_access_token
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_crud.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    new_user = user_crud.create_user(db, user_data)
    return new_user


@router.post("/login", response_model=Token)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
