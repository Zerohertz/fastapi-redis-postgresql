from sqlalchemy.orm import Session

from app import models, schemas
from app.core import pwd_context
from app.database import Base
from app.logger import logger


def create_account(db: Session, account: schemas.AccountCreate):
    logger.debug(f"[crud] create_account: {account}")
    account_dict = {
        **account.dict(),
        **{
            "password": pwd_context.hash(account.password),
        },
    }
    return _create(db, models.Account(**account_dict))


def get_account(db: Session, account_id: int):
    logger.debug(f"[crud] get_account: {account_id}")
    return _fetch_by_id(db, models.Account, account_id)


def get_account_by_username(db: Session, username: str):
    logger.debug(f"[crud] get_account_by_username: {username}")
    return _fetch_by_id(db, models.Account, username, db_col="username")


def _fetch_by_id(db: Session, db_model: Base, db_id: int, db_col: str = "id"):
    logger.debug(f"[crud] _fetch_by_id: {db_model}")
    return db.query(db_model).filter(getattr(db_model, db_col) == db_id).first()


def _create(db: Session, db_model: Base):
    logger.debug(f"[crud] _create: {db_model}")
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model
