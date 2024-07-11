import redis.asyncio as redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.logger import logger

engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
RedisPool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


def get_postgres():
    logger.info("[database] get_postgres: Connect")
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        logger.info("[database] get_postgres: Close")


async def get_redis():
    logger.info("[database] get_redis: Connect")
    try:
        client = await redis.Redis(connection_pool=RedisPool)
        yield client
    finally:
        await client.aclose()
        logger.info("[database] get_redis: Close")
