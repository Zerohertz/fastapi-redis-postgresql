import hashlib
import secrets
from datetime import timedelta

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


def authenticate_account(db: DbSession, email: str, password: str):
    account = crud.get_account_by_email(db, email)
    if not account:
        return False
    if not pwd_context.verify(password, account.password):
        return False
    return account


def create_access_token(*, account: Account, expires_delta: timedelta = None):
    if not expires_delta:
        expires_delta = timedelta(minutes=15)
    token = secrets.token_hex()
    hashed_token = hash_token(token, settings.REDIS_TOKEN)
    session_db = get_redis()
    logger.debug(f"[auth] create_access_token: {account.email}")
    session_db.hmset(hashed_token, {"email": account.email})
    session_db.expire(hashed_token, expires_delta)
    return token


def get_account(
    token: str = Depends(oauth2_scheme), db: DbSession = Depends(get_postgres)
):
    session_db = get_redis()
    hashed_token = hash_token(token, settings.REDIS_TOKEN)
    logger.debug(f"""[auth] get_data: {hashed_token}""")
    data = session_db.hgetall(hashed_token)
    if not data:
        raise CREDENTIALS_EXCEPTION
    data = {key.decode(): value.decode() for key, value in data.items()}
    logger.debug(f"""[auth] get_data: {data["email"]}""")
    account = crud.get_account_by_email(db, data["email"])
    if account is None:
        raise CREDENTIALS_EXCEPTION
    return account
