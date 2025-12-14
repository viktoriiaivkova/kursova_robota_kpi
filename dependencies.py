from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config import Settings, load_settings
from src.database import get_db
from src.repo import UserRepository, AccountRepository
#importing and cashing config settings
@lru_cache()
def get_settings() -> Settings:
    return load_settings()

ConfigDep = Depends(get_settings)


#db utils
def get_db_session(db: Session = Depends(get_db)):
    return db

user_repo_singleton = UserRepository(db=None)
account_repo_singleton = AccountRepository(db=None)


def get_user_repository(db: Session = Depends(get_db)):
    user_repo_singleton.db = db
    return user_repo_singleton

def get_account_repository(db: Session = Depends(get_db)):
    account_repo_singleton.db = db
    return account_repo_singleton

UserRepo = Depends(get_user_repository)
AccountRepo = Depends(get_account_repository)
