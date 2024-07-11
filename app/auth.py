import hashlib
import secrets
from datetime import timedelta

import redis.asyncio as redis
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session as DbSession
from starlette.status import HTTP_401_UNAUTHORIZED

from app import crud
from app.config import settings
from app.core import oauth2_scheme, pwd_context
from app.database import get_postgres, get_redis
from app.logger import logger
from app.models import Account

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
LOGIN_EXCEPTION = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)


def hash_token(token, secret_key):
    return hashlib.sha256((secret_key + token).encode("utf-8")).hexdigest()


def authenticate_account(db: DbSession, username: str, password: str):
    account = crud.get_account_by_username(db, username)
    if not account:
        return False
    if not pwd_context.verify(password, account.password):
        return False
    return account


async def create_access_token(
    *,
    account: Account,
    expires_delta: timedelta,
    cache: redis.Redis,
):
    token = secrets.token_hex()
    hashed_token = hash_token(token, settings.REDIS_TOKEN)
    logger.debug(f"[auth] create_access_token: {account.username}")
    await cache.hmset(hashed_token, {"username": account.username})
    await cache.expire(hashed_token, expires_delta)
    return token


async def get_account(
    token: str = Depends(oauth2_scheme),
    db: DbSession = Depends(get_postgres),
    cache: redis.Redis = Depends(get_redis),
):
    hashed_token = hash_token(token, settings.REDIS_TOKEN)
    logger.debug(f"""[auth] get_data: {hashed_token}""")
    data = await cache.hgetall(hashed_token)
    if not data:
        raise CREDENTIALS_EXCEPTION
    data = {key: value for key, value in data.items()}
    logger.debug(f"""[auth] get_data: {data["username"]}""")
    account = crud.get_account_by_username(db, data["username"])
    if account is None:
        raise CREDENTIALS_EXCEPTION
    return account
