from app.repositories.AssignmentRepository import AssignmentRepository
from app.repositories.ProjectRepository import ProjectRepository
from sqlalchemy.orm import Session

from app.core.exceptions import AccessDeniedError, ProjectAssignmentRequiredError, UserNotFoundError
from app.models.RoleModel import RoleEnum as RE
from app.repositories.UserRepository import UserRepository
import app.schemas.UserSchema as UserSchema


class UserService:

    @staticmethod
    def get_users(
        current_user: dict,
        roles: list[RE],
        manager_id: int | None,
        is_alive: list[int],
        project_ids: list[int] | None,
        has_manager: list[ bool ],
        db: Session,
    ):
        if RE.ADMIN not in current_user.get("user_roles"):
            if manager_id is not None and manager_id != current_user.get("user_id"):
                raise AccessDeniedError()
            else:
                manager_id = current_user.get("user_id")

        if project_ids is not None and RE.ADMIN not in current_user.get("user_roles"):
            if not ProjectRepository.are_projects_assigned( project_ids, current_user.get("user_id"), db):
                raise ProjectAssignmentRequiredError()
        
        if has_manager is None:
            has_manager = [ True, False ]
        
        users_data = UserRepository.get_users(db, roles, manager_id, is_alive, project_ids, has_manager, current_user)
        return [UserSchema.UserResponse(**u) for u in users_data]

    @staticmethod
    def get_user_by_id(user_id: int, current_user: dict, db: Session):
        user_roles = current_user.get("user_roles", [])
        current_user_id = current_user.get("user_id")

        if RE.ADMIN not in user_roles and RE.MANAGER not in user_roles:
            if user_id != current_user_id:
                raise AccessDeniedError()
        
        user_data = UserRepository.get_user_by_id(user_id, db)
        if not user_data:
            raise UserNotFoundError()
        
        if RE.ADMIN in user_roles:
            pass
        elif current_user_id == user_id:
            pass
        elif AssignmentRepository.can_view_users_projects(current_user_id, [ user_id ], db):
            pass
        elif user_data[ "user" ].manager_id is None:
            pass
        else:
            raise AccessDeniedError()

        return UserSchema.UserResponse(**user_data["user"]._mapping, roles=user_data["roles"])



    @staticmethod
    def create_user(data: UserSchema.CreateUserRequest, db: Session):
        user = UserRepository.create_user(data, db)
        roles = [r.value for r in data.roles] if data.roles else [RE.EMPLOYEE.value]
        return UserSchema.CreateUserResponse(
            id=user.id,
            name=user.name,
            userid=user.userid,
            username=data.username,
            phone_number=user.phone_number,
            company_mail=user.company_mail,
            password=data.password,
            roles=roles,
            manager_id=user.manager_id,
            manager_name=UserRepository.get_user_by_id(user.manager_id, db)['user'].name if user.manager_id else None
        )

    @staticmethod
    def edit_user(user_id: int, data: UserSchema.EditUserRequest, db: Session):
        result = UserRepository.edit_user(user_id, data, db)
        if result is None:
            raise UserNotFoundError()
        user, username = result
        return UserSchema.UserResponse(
            id=user.id,
            userid = user.userid,
            username=username,
            name = user.name,
            manager_id=user.manager_id,
            manager_name=UserRepository.get_user_by_id(user.manager_id, db)[ 'user' ].name if user.manager_id else None,
            phone_number=user.phone_number,
            roles=UserRepository.get_user_roles(user.id, db),
            company_mail=user.company_mail,
            is_alive=user.is_alive
        )

    @staticmethod
    def update_password(user_id: int, data: UserSchema.UpdatePasswordRequest, db: Session):
        user = UserRepository.update_password(user_id, data, db)
        if not user:
            raise UserNotFoundError()
        return {"message": "Password updated successfully"}

    @staticmethod
    def delete_user(user_id: int, db: Session):
        user = UserRepository.soft_delete_user(user_id, db)
        if not user:
            raise UserNotFoundError()
        return {"message": "User soft deleted successfully"}
