import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "No Food Waste"
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "set it up in vecel environment variables"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    # DB_USERNAME: str = os.getenv("DB_USERNAME")
    # DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    # DB_HOST: str = os.getenv("DB_HOST")
    DB_SCHEMA: str = os.getenv("DB_SCHEMA", "wfnfw")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "already configured in vecel environment variables"
    )
    print(DATABASE_URL)
    GOOGLE_DRIVE_FOLDER_ID: str = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "")
    GOOGLE_REFRESH_TOKEN: str = os.getenv("GOOGLE_REFRESH_TOKEN", "")

    # Breakglass (emergency admin bootstrap)
    BREAKGLASS_MOBILE: str = os.getenv("BREAKGLASS_MOBILE", "0000000000")
    BREAKGLASS_PASSWORD_HASH: str = os.getenv("BREAKGLASS_PASSWORD_HASH", "")

    # Google API endpoint URLs — fixed by Google, centralised here for consistency
    GOOGLE_DRIVE_FILES_URL: str = "https://www.googleapis.com/drive/v3/files"
    GOOGLE_DRIVE_UPLOAD_URL: str = (
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
    )
    GOOGLE_DRIVE_TOKEN_URL: str = "https://oauth2.googleapis.com/token"

    class Config:
        env_file = ".env"


settings = Settings()
