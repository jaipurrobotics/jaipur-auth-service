import uvicorn
from fastapi import FastAPI

from app.core.database import Base, engine
from app.routers import auth

def create_app() -> FastAPI:
    app = FastAPI(title="Jaipur Auth Service", version="1.0.0")

    # For local dev only: create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Include auth routes
    app.include_router(auth.router, prefix="/auth", tags=["auth"])

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
