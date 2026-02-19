from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from typing import AsyncGenerator
import logging
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger(__name__)


def _mask_password(url: str) -> str:
    # crude masking for logs
    try:
        before, after = url.split("@", 1)
        if ":" in before:
            userpart = before.split("//", 1)[1]
            user, _ = userpart.split(":", 1)
            return url.replace(f"{user}:", f"{user}:***@")
    except Exception:
        pass
    return url


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Please set it in the environment or .env file.")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")

logger.info("Using DATABASE_URL=%s", _mask_password(DATABASE_URL))

# asyncpg does not accept `sslmode` keyword; convert to connect_args
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
