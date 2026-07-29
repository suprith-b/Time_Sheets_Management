from app.repositories.ProjectRepository import ProjectRepository
from app.utils.security import hash_password
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.RoleModel import RoleEnum
from app.repositories.UserRepository import UserRepository
import app.schemas.UserSchema as UserSchema


class UserService:

    @staticmethod
    def get_users(
        current_user: dict,
        roles: list[RoleEnum],
        manager_id: int | None,
        is_alive: list[int],
        project_ids: list[int] | None,
        db: Session,
    ):
        if "admin" not in current_user.get("user_roles") and manager_id != current_user.get("user_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        if project_ids is None and "admin" not in current_user.get("user_roles"):
            if not ProjectRepository.is_assigned( project_ids, current_user.get("user_id"), db):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more projects are not assigned to you",
                )
                
        users_data = UserRepository.get_users(db, roles, manager_id, is_alive, project_ids, current_user)
        return [UserSchema.UserResponse(**u) for u in users_data]

    @staticmethod
    def get_user_by_id(user_id: int, current_user: dict, db: Session):
        user_roles = current_user.get("user_roles", [])
        current_user_id = current_user.get("user_id")

        if "admin" not in user_roles and "manager" not in user_roles:
            if user_id != current_user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to access this resource",
                )

        user_data = UserRepository.get_user_detail_by_id(user_id, db)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if "admin" not in user_roles and "manager" in user_roles:
            if user_id != current_user_id and user_data["manager_id"] != current_user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to access this resource",
                )

        return UserSchema.UserDetailResponse(**user_data)



    @staticmethod
    def create_user(data: UserSchema.CreateUserRequest, db: Session):
        user = UserRepository.create_user(data, db)
        roles = [r.value for r in data.roles] if data.roles else [RoleEnum.EMPLOYEE.value]
        return UserSchema.CreateUserResponse(
            id=user.id,
            name=user.name,
            userid=user.userid,
            username=data.username,
            personal_mail=user.personal_mail,
            company_mail=user.company_mail,
            password=data.password,
            roles=roles,
        )

    @staticmethod
    def edit_user(user_id: int, data: UserSchema.EditUserRequest, db: Session):
        user, username = UserRepository.edit_user(user_id, data, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        print( "user:\n\n\n\n\n\n", user )
        return UserSchema.UserResponse(
            id=user.id,
            userid = user.userid,
            username=username,
            name = user.name,
            manager_id=None,
            manager_name=None,
            roles=[],
            is_alive=user.is_alive
        )

    @staticmethod
    def update_password(user_id: int, data: UserSchema.UpdatePasswordRequest, db: Session):
        user = UserRepository.update_password(user_id, data, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"message": "Password updated successfully"}

    @staticmethod
    def delete_user(user_id: int, db: Session):
        user = UserRepository.soft_delete_user(user_id, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"message": "User soft deleted successfully"}
