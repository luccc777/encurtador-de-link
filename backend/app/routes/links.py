from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.crud.link_crud import (
    create_link,
    get_link_by_slug,
    get_links_by_user,
    delete_link,
    increment_clicks,
)
from app.schemas.link_schema import LinkCreate, LinkResponse
from app.models.user import User

router = APIRouter(prefix="/links", tags=["Links"])


# --------------------- ROTAS --------------------- #

@router.post("/", response_model=LinkResponse, status_code=status.HTTP_201_CREATED)
def create_user_link(
    link_in: LinkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        db_link = create_link(db=db, link=link_in, user_id=current_user.id)
        return db_link
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=list[LinkResponse])
def list_user_links(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retorna todos os links criados pelo usuário autenticado."""
    links = get_links_by_user(db, user_id=current_user.id)
    return links


@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_link(
    link_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deleta um link pertencente ao usuário autenticado."""
    deleted = delete_link(db, link_id=link_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Link não encontrado ou não pertence ao usuário")
    return


@router.get("/{slug}")
def redirect_short_link(slug: str, db: Session = Depends(get_db)):
    """Redireciona o visitante para a URL original com base no slug."""
    link = get_link_by_slug(db, slug)
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")
    increment_clicks(db, slug)
    return RedirectResponse(url=link.original_url)
