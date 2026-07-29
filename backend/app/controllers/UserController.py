from app.utils.security import hash_password
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.RoleModel import RoleEnum
import app.schemas.UserSchema as UserSchema
from app.services.UserService import UserService
from app.utils.RoleValidation import RoleValidation

router = APIRouter(prefix="/users")


@router.get("", response_model=list[UserSchema.UserResponse])
def get_users(
    roles: list[RoleEnum] = Query(default_factory=lambda: list(RoleEnum)),
    manager_id: int | None = Query(default=None),
    is_alive: list[int] = Query(default=[1]),
    project_ids: list[int] | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin", "manager"])
    return UserService.get_users(current_user, roles, manager_id, is_alive, project_ids, db)


@router.get("/{user_id}", response_model=UserSchema.UserDetailResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin", "manager", "employee"])
    return UserService.get_user_by_id(user_id, current_user, db)




@router.post("", response_model=UserSchema.CreateUserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserSchema.CreateUserRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin"])
    return UserService.create_user(data, db)


@router.patch("/{user_id}", response_model=UserSchema.UserResponse)
def edit_user(
    user_id: int,
    data: UserSchema.EditUserRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin"])
    return UserService.edit_user(user_id, data, db)


@router.patch("/password/{user_id}")
def update_password(
    user_id: int,
    data: UserSchema.UpdatePasswordRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return UserService.update_password(user_id, data, db)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin"])
    return UserService.delete_user(user_id, db)
