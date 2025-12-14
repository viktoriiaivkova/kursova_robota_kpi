import logging

from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from src import models, schemas

logger = logging.getLogger(__name__)
class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> models.User | None:
        logger.info(f"Fetching user with ID: {user_id}")
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_by_email(self, email: str) -> models.User | None:
        logger.info(f"Searching for user by email: {email}")
        return self.db.query(models.User).filter(models.User.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[models.User]:
        logger.info(f"Fetching users list (skip={skip}, limit={limit})")
        return self.db.query(models.User).offset(skip).limit(limit).all()

    def create(self, user_dto: schemas.UserCreateDTO) -> models.User:
        logger.info(f"Creating new user: {user_dto.email}")
        db_user = models.User(**user_dto.model_dump())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        logger.info(f"User created successfully with ID: {db_user.id}")
        return db_user

    def update(self, db_user: models.User, user_dto: schemas.UserCreateDTO) -> models.User:
        logger.info(f"Updating user ID: {db_user.id}")
        db_user.username = user_dto.username
        db_user.email = user_dto.email
        self.db.commit()
        self.db.refresh(db_user)
        logger.info(f"User ID: {db_user.id} updated successfully")
        return db_user

    def delete(self, db_user: models.User):
        logger.warning(f"Deleting user ID: {db_user.id}")
        self.db.delete(db_user)
        self.db.commit()
        logger.info(f"User ID: {db_user.id} deleted")

    def delete_all(self):
        logger.warning("Deleting all users")
        self.db.query(models.User).delete()
        self.db.commit()



class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def count_by_user_id(self, user_id: int) -> int:
        return self.db.query(func.count(models.Account.id)) \
            .filter(models.Account.user_id == user_id) \
            .scalar()
    def get_by_id(self, account_id: int) -> models.Account | None:
        logger.info(f"Fetching account with ID: {account_id}")
        return self.db.query(models.Account).filter(models.Account.id == account_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[models.Account]:
        logger.info(f"Fetching accounts list (skip={skip}, limit={limit})")
        return self.db.query(models.Account).offset(skip).limit(limit).all()

    def create(self, account_dto: schemas.AccountCreateDTO) -> models.Account:
        logger.info(f"Creating account for User ID: {account_dto.user_id}")
        db_account = models.Account(**account_dto.model_dump())
        self.db.add(db_account)
        self.db.commit()
        self.db.refresh(db_account)
        logger.info(f"Account created with ID: {db_account.id}")
        return db_account

    def update(self, db_account: models.Account, account_dto: schemas.AccountBaseDTO) -> models.Account:
        logger.info(f"Updating account ID: {db_account.id}")
        db_account.acc_name = account_dto.acc_name
        db_account.balance = account_dto.balance
        db_account.user_id = account_dto.user_id
        self.db.commit()
        self.db.refresh(db_account)
        logger.info(f"Account ID: {db_account.id} updated successfully")
        return db_account

    def delete(self, db_account: models.Account):
        logger.warning(f"Deleting account ID: {db_account.id}")
        self.db.delete(db_account)
        self.db.commit()
        logger.info(f"Account ID: {db_account.id} deleted")

    def delete_all(self):
        logger.warning("Deleting ALL accounts")
        self.db.query(models.Account).delete()
        self.db.commit()