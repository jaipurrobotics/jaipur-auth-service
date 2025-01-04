import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "mypassword"
    DB_NAME: str = "jaipur_auth"

    class Config:
        env_file = ".env"   # optional, for local development

settings = Settings()
