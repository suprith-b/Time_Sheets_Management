from app.repositories import ProjectRepository
from app.repositories.UserRepository import UserRepository
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.AssignmentRepository import AssignmentRepository
import app.schemas.AssignmentSchema as AssignmentSchema
from app.models.RoleModel import RoleEnum


class AssignmentService:

    @staticmethod
    def assign_users_to_manager(
        manager_id: int,
        data: AssignmentSchema.AssignUsersToManagerRequest,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        if not UserRepository.check_user_roles([manager_id], RoleEnum.MANAGER, db):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Manager not found",
            )
        if not UserRepository.check_user_roles( data.employee_ids, RoleEnum.EMPLOYEE, db):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more employees not found",
            )

        AssignmentRepository.update_users_manager(manager_id, data.employee_ids, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Employees successfully assigned to manager")

    @staticmethod
    def assign_projects(
        data: AssignmentSchema.ProjectAssignmentRequest,
        current_user: dict,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        if "admin" not in current_user.get("user_roles", []):
            manager_id = current_user["user_id"]
            if not ProjectRepository.is_assigned(data.project_ids, manager_id, db):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="One or more projects are not assigned to current manager",
                )
            if not AssignmentRepository.are_users_managed_by(manager_id, data.user_ids, db):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="One or more users do not belong to current manager",
                )

        AssignmentRepository.assign_projects(data.user_ids, data.project_ids, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Projects successfully assigned")

    @staticmethod
    def deassign_projects(
        data: AssignmentSchema.ProjectAssignmentRequest,
        current_user: dict,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        if "admin" not in current_user.get("user_roles", []):
            manager_id = current_user["user_id"]
            if not ProjectRepository.is_assigned(data.project_ids, manager_id, db):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="One or more projects are not assigned to current manager",
                )
            if not AssignmentRepository.are_users_managed_by(manager_id, data.user_ids, db):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="One or more users do not belong to current manager",
                )

        AssignmentRepository.deassign_projects(data.user_ids, data.project_ids, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Projects successfully deassigned")

    @staticmethod
    def assign_roles(
        data: AssignmentSchema.RoleAssignmentRequest,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        AssignmentRepository.assign_roles(data.user_ids, data.roles, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Roles successfully assigned")

    @staticmethod
    def deassign_roles(
        data: AssignmentSchema.RoleAssignmentRequest,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        AssignmentRepository.deassign_roles(data.user_ids, data.roles, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Roles successfully deassigned")

    @staticmethod
    def sync_users_to_project(
        project_id: int,
        data: AssignmentSchema.AssignUsersToProjectRequest,
        current_user: dict,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        if "admin" not in current_user.get("user_roles", []):
            manager_id = current_user["user_id"]
            if not ProjectRepository.is_assigned([project_id], manager_id, db):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Project is not assigned to current manager",
                )
            if not AssignmentRepository.are_users_managed_by(manager_id, data.user_ids, db):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="One or more users do not belong to current manager",
                )

        AssignmentRepository.sync_users_to_project(project_id, data.user_ids, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Users successfully synced to project")

    @staticmethod
    def sync_projects_to_user(
        user_id: int,
        data: AssignmentSchema.AssignProjectsToUserRequest,
        current_user: dict,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        if "admin" not in current_user.get("user_roles", []):
            manager_id = current_user["user_id"]
            if not AssignmentRepository.are_users_managed_by(manager_id, [user_id], db):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User does not belong to current manager",
                )
            if not ProjectRepository.is_assigned(data.project_ids, manager_id, db):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="One or more projects are not assigned to current manager",
                )

        AssignmentRepository.sync_projects_to_user(user_id, data.project_ids, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Projects successfully synced to user")

    @staticmethod
    def sync_roles_to_user(
        user_id: int,
        data: AssignmentSchema.AssignRolesToUserRequest,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        AssignmentRepository.sync_roles_to_user(user_id, data.roles, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Roles successfully synced to user")

