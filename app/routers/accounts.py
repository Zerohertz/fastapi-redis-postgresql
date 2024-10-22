from datetime import timedelta

import redis.asyncio as redis
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import auth, crud, models, schemas
from app.config import settings
from app.database import get_postgres, get_redis
from app.logger import logger

router = APIRouter()


@router.post("/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_postgres)):
    logger.info(
        f"[routers/accounts] create_account: Checking {account.username} was created..."
    )
    is_created = auth.authenticate_account(db, account.username, account.password)
    if is_created:
        logger.info(
            f"[routers/accounts] create_account: {account.username} was already created"
        )
        return is_created
    logger.info(f"[routers/accounts] create_account: Creating {account.username}")
    return crud.create_account(db, account)


@router.get("/me/", response_model=schemas.Account)
def read_account_me(account: models.Account = Depends(auth.get_account)):
    logger.info(f"[routers/accounts] read_account_me: {account.username}")
    return account


@router.post("/token/", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_postgres),
    cache: redis.Redis = Depends(get_redis),
):
    logger.info(f"[routers/accounts] login_for_access_token: {form_data.username}")
    account = auth.authenticate_account(db, form_data.username, form_data.password)
    if not account:
        raise auth.LOGIN_EXCEPTION
    access_token_expires = timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
    access_token = await auth.create_access_token(
        account=account, expires_delta=access_token_expires, cache=cache
    )
    return {"access_token": access_token, "token_type": "bearer"}
