import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "No Food Waste"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    #DB_USERNAME: str = os.getenv("DB_USERNAME")
    #DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    #DB_HOST: str = os.getenv("DB_HOST")
    DB_SCHEMA: str =  os.getenv("DB_SCHEMA")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    class Config:
        env_file = ".env"


settings = Settings()
