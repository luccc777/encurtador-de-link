from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import auth, links, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="encurtador API",
            description="Api para encurtar links",
            version="0.1.0")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(links.router, tags=["Links"])
app.include_router(users.router, tags=["Users"])