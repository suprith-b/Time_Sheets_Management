from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import app.schemas.UserSchema as UserSchema
from app.repositories.ProjectAssignmentRepository import ProjectAssignmentRepository
from app.repositories.UserRepository import UserRepository
from app.repositories.ProjectRepository import ProjectRepository
import app.schemas.ProjectAssignmentSchema as ProjectAssignmentSchema
from app.models.RoleModel import RoleEnum

class UserService:

    @staticmethod
    def get_users(current_user: dict, roles: list[RoleEnum], db: Session):
        users = UserRepository.get_all_users(current_user, roles, db)
        return [UserSchema.UserResponse.model_validate(user) for user in users]

    @staticmethod
    def get_user(current_user: dict, user_id: int, db: Session):
        user = UserRepository.get_user_by_id(user_id, current_user, db)
        if user is None:
            return None
        return UserSchema.UserResponse.model_validate(user)

    @staticmethod
    def create_user(data: UserSchema.CreateUserRequest, db: Session):
        user = UserRepository.create_user(data, db)
        return UserSchema.CreateUserResponse.model_validate(user)

    @staticmethod
    def delete_user(user_id: int, db: Session):
        user = UserRepository.delete_user(user_id, db)
        if user is None:
            return None
        return UserSchema.UserResponse.model_validate(user)

    @staticmethod
    def edit_user(user_id: int, data: UserSchema.EditUser, db: Session):
        user = UserRepository.edit_user(user_id, data, db)
        if user is None:
            return None
        return UserSchema.UserResponse.model_validate(user)

    @staticmethod
    def assign_projects(
        user_id: int,
        data: ProjectAssignmentSchema.AssignProjectsRequest,
        current_user: dict,
        db: Session,
    ):
        user = UserRepository.get_user_by_id(user_id, current_user, db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        project_ids = data.project_ids
        assigned_projects = {
            project.id
            for project, manager_id in ProjectRepository.get_all_projects(
                current_user,
                db,
            )
        }
        invalid_project_ids = [
            project_id
            for project_id in project_ids
            if project_id not in assigned_projects
        ]
        if invalid_project_ids:
            detail = (
                "One or more projects do not exist"
                if current_user["user_role"] == "admin"
                else "One or more projects are not assigned to you"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": detail, "project_ids": invalid_project_ids},
            )

        ProjectAssignmentRepository.assign_projects(user_id, project_ids, db)
        return ProjectAssignmentSchema.AssignProjectsResponse(
            user_id=user_id,
            project_ids=project_ids
        )