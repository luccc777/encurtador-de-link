from sqlalchemy.orm import Session
from app.models.link import Link
from app.schemas.link_schema import LinkCreate
from datetime import datetime, UTC
import string, random

def generate_slug(length: int = 6) -> str:
    """Gera um slug curto e aleatório."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def get_link_by_user_and_url(db: Session, user_id: int, original_url: str) -> Link | None:
    """Verifica se o usuário já tem um link com a mesma URL."""
    return db.query(Link).filter(
        Link.user_id == user_id,
        Link.original_url == original_url
    ).first()

def create_link(db: Session, link: LinkCreate, user_id: int) -> Link:
    
    existing_link = get_link_by_user_and_url(db, user_id, str(link.original_url))
    if existing_link:
        raise ValueError("Você já possui um link encurtado para esta URL")
    
    max_attempts = 10
    for _ in range(max_attempts):
        slug = generate_slug()
        # Verifica se o slug já existe
        existing_link = get_link_by_slug(db, slug)
        if not existing_link:
            break
    else:
        # Se não conseguiu gerar um slug único após várias tentativas, aumenta o tamanho
        slug = generate_slug(length=8)
        existing_link = get_link_by_slug(db, slug)
        if existing_link:
            raise ValueError("Não foi possível gerar um slug único")

    # Gera a short_url apenas com o slug (o frontend pode adicionar o domínio)
    short_url = slug

    db_link = Link(
        slug=slug,
        original_url=str(link.original_url),  # Converte AnyUrl para string
        short_url=short_url,
        user_id=user_id,
        created_at=datetime.now(UTC),
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

def get_link_by_slug(db: Session, slug: str) -> Link | None:
    return db.query(Link).filter(Link.slug == slug).first()

def increment_clicks(db: Session, slug: str) -> None:
    link = get_link_by_slug(db, slug)
    if link:
        link.clicks += 1
        db.commit()
        db.refresh(link)

def get_links_by_user(db: Session, user_id: int) -> list[Link]:
    return db.query(Link).filter(Link.user_id == user_id).all()

def delete_link(db: Session, link_id: int, user_id: int) -> bool:
    link = db.query(Link).filter(Link.id == link_id, Link.user_id == user_id).first()
    if not link:
        return False
    db.delete(link)
    db.commit()
    return True
