from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import auth, crud, models, schemas
from app.config import settings
from app.database import get_postgres

router = APIRouter()


@router.post("/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_postgres)):
    return crud.create_account(db, account)


@router.get("/me/", response_model=schemas.Account)
def read_account_me(account: models.Account = Depends(auth.get_account)):
    return account


@router.post("/token/", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_postgres),
):
    account = auth.authenticate_account(db, form_data.username, form_data.password)
    if not account:
        raise auth.LOGIN_EXCEPTION
    access_token_expires = timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        account=account,
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
