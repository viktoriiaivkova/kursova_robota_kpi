from fastapi import APIRouter, HTTPException, status
from typing import List

from fastapi_cache.decorator import cache

from src import schemas
from src.repo import UserRepository
from src.dependencies import UserRepo
from fastapi_cache import FastAPICache


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.post("/",
             response_model=schemas.UserResponseDTO,
             status_code=status.HTTP_201_CREATED,
             summary="Create new user")
async def create_user(user_dto: schemas.UserCreateDTO, repo: UserRepository = UserRepo):
    db_user = repo.get_by_email(user_dto.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user_dto.email} already exists."
        )
    await FastAPICache.clear(namespace="users")
    return repo.create(user_dto=user_dto)


@router.get("/",
            response_model=List[schemas.UserResponseDTO],
            summary="Get list of all users")
@cache(expire=20, namespace="users")
async def get_users_list(skip: int = 0, limit: int = 100,
                   repo: UserRepository = UserRepo):
    users = repo.get_all(skip=skip, limit=limit)
    return [schemas.UserResponseDTO.model_validate(u) for u in users]

@router.get("/{user_id}",
            response_model=schemas.UserResponseDTO,
            summary="Get user by ID")
def get_user_by_id(user_id: int, repo: UserRepository = UserRepo):
    db_user = repo.get_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
@router.put("/{user_id}",
            response_model=schemas.UserResponseDTO,
            summary="Update user by ID")
async def update_user(user_id: int, user_dto: schemas.UserCreateDTO,
                repo: UserRepository = UserRepo):
    db_user = repo.get_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user_dto.email != db_user.email:
        existing_user = repo.get_by_email(user_dto.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email {user_dto.email} is already taken."
            )
    await FastAPICache.clear(namespace="users")
    return repo.update(db_user=db_user, user_dto=user_dto)
@router.delete("/{user_id}",
               status_code=status.HTTP_200_OK,
               summary="Delete user by ID")
async def delete_user_by_id(user_id: int, repo: UserRepository = UserRepo):
    db_user = repo.get_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    repo.delete(db_user)
    await FastAPICache.clear(namespace="users")
    return {"detail": f"User with id {user_id} and all their accounts deleted"}
@router.delete("/",
               status_code=status.HTTP_200_OK,
               summary="Delete all users")
async def delete_all_users(repo: UserRepository = UserRepo):
    repo.delete_all()
    await FastAPICache.clear(namespace="users")
    return {"detail": "All users and accounts have been deleted"}