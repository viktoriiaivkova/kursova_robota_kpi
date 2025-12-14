from fastapi import APIRouter, HTTPException, status
from typing import List

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from src import schemas
from src.config import Settings
from src.repo import AccountRepository, UserRepository
from src.dependencies import AccountRepo, UserRepo, ConfigDep

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.post("/",
             response_model=schemas.AccountResponseDTO,
             status_code=status.HTTP_201_CREATED,
             summary="Create account")
async def create_account(account_dto: schemas.AccountCreateDTO,
                   repo: AccountRepository = AccountRepo,
                   user_repo: UserRepository = UserRepo,
                   settings: Settings = ConfigDep):
    if not settings.business_rules.allow_account_creation:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account creation is currently disabled by administrator."
        )
    db_user = user_repo.get_by_id(account_dto.user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {account_dto.user_id} not found."
        )
    current_count = repo.count_by_user_id(account_dto.user_id)
    limit = settings.business_rules.max_accounts_per_user

    if current_count >= limit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User reached the limit of {limit} accounts."
        )
    await FastAPICache.clear(namespace="accounts")
    return repo.create(account_dto=account_dto)


@router.get("/",
            response_model=List[schemas.AccountResponseDTO],
            summary="Get all accounts")
@cache(expire=20, namespace="accounts")
async def get_accounts_list(skip: int = 0, limit: int = 100,
                      repo: AccountRepository = AccountRepo):
    accounts = repo.get_all(skip=skip, limit=limit)
    return [schemas.AccountResponseDTO.model_validate(u) for u in accounts]


@router.get("/{account_id}",
            response_model=schemas.AccountResponseDTO,
            summary="Get an account by ID")
def get_account_by_id(account_id: int, repo: AccountRepository = AccountRepo):
    db_account = repo.get_by_id(account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@router.put("/{account_id}",
            response_model=schemas.AccountResponseDTO,
            summary="Update account by ID")
async def update_account(account_id: int, account_dto: schemas.AccountCreateDTO,
                   repo: AccountRepository = AccountRepo,
                   user_repo: UserRepository = UserRepo):
    db_account = repo.get_by_id(account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    if db_account.user_id != account_dto.user_id:
        db_user = user_repo.get_by_id(account_dto.user_id)
        if db_user is None:
            raise HTTPException(
                status_code=404,
                detail=f"User with id {account_dto.user_id} not found."
            )
    await FastAPICache.clear(namespace="accounts")
    return repo.update(db_account=db_account, account_dto=account_dto)


@router.delete("/{account_id}",
               status_code=status.HTTP_200_OK,
               summary="Delete account by ID")
async def delete_account_by_id(account_id: int, repo: AccountRepository = AccountRepo):
    db_account = repo.get_by_id(account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    repo.delete(db_account)
    await FastAPICache.clear(namespace="accounts")
    return {"detail": f"Account with id {account_id} deleted"}


@router.delete("/",
               status_code=status.HTTP_200_OK,
               summary="Delete all accounts")
async def delete_all_accounts(repo: AccountRepository = AccountRepo):
    repo.delete_all()
    await FastAPICache.clear(namespace="accounts")
    return {"detail": "All accounts have been deleted"}