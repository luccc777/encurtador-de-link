from pydantic import BaseModel, AnyUrl
from datetime import datetime

class LinkCreate(BaseModel):
    original_url: AnyUrl

class LinkResponse(BaseModel):
    id: int
    slug: str
    original_url: AnyUrl
    short_url: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True
