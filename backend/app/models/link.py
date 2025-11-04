from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    original_url = Column(String, nullable=False)
    short_url = Column(String, nullable=False)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="links")
