from prisma import Prisma

from app.core.config import get_settings

prisma = Prisma()


async def connect_db() -> None:
    settings = get_settings()
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL is not set")
    if not prisma.is_connected():
        await prisma.connect()


async def disconnect_db() -> None:
    if prisma.is_connected():
        await prisma.disconnect()
