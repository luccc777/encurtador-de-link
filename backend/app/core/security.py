from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.utils.jwt_handler import decode_access_token
from app.crud.user_crud import get_user_by_email
from app.core.database import get_db
from app.models.user import User

# URL do endpoint de login (usada pelo Swagger, mas também nas rotas)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Obtém o usuário atual a partir do token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise credentials_exception

    email: str = payload.get("sub")
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    return user
