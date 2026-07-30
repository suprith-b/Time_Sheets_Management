from app.repositories import ProjectRepository
from app.repositories.UserRepository import UserRepository
from sqlalchemy.orm import Session

from app.repositories.AssignmentRepository import AssignmentRepository
import app.schemas.AssignmentSchema as AssignmentSchema
from app.models.RoleModel import RoleEnum
from app.core.exceptions import ManagerNotFoundError, ManagedUserRequiredError, ProjectAssignmentRequiredError, ProjectNotFoundError, UserNotFoundError


class AssignmentService:

    @staticmethod
    def assign_users_to_manager(
        manager_id: int,
        data: AssignmentSchema.AssignUsersToManagerRequest,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        if not UserRepository.check_user_roles([manager_id], RoleEnum.MANAGER, db):
            raise ManagerNotFoundError()
        if not UserRepository.check_user_roles( data.employee_ids, RoleEnum.EMPLOYEE, db):
            raise UserNotFoundError("One or more employees not found")

        AssignmentRepository.update_users_manager(manager_id, data.employee_ids, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Employees successfully assigned to manager")

    @staticmethod
    def assign_projects(
        data: AssignmentSchema.ProjectAssignmentRequest,
        current_user: dict,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        if not UserRepository.are_users_present(data.user_ids, db):
            raise UserNotFoundError("One or more users not found")
        if not ProjectRepository.are_projects_present(data.project_ids, db):
            raise ProjectNotFoundError("One or more projects not found")

        if "admin" not in current_user.get("user_roles", []):
            manager_id = current_user["user_id"]
            if not ProjectRepository.is_assigned(data.project_ids, manager_id, db):
                raise ProjectAssignmentRequiredError("One or more projects are not assigned to current manager")
            if not AssignmentRepository.are_users_managed_by(manager_id, data.user_ids, db):
                raise ManagedUserRequiredError()

        AssignmentRepository.assign_projects(data.user_ids, data.project_ids, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Projects successfully assigned")

    @staticmethod
    def deassign_projects(
        data: AssignmentSchema.ProjectAssignmentRequest,
        current_user: dict,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        if not UserRepository.are_users_present(data.user_ids, db):
            raise UserNotFoundError("One or more users not found")
        if not ProjectRepository.are_projects_present(data.project_ids, db):
            raise ProjectNotFoundError("One or more projects not found")

        if "admin" not in current_user.get("user_roles", []):
            manager_id = current_user["user_id"]
            if not ProjectRepository.is_assigned(data.project_ids, manager_id, db):
                raise ProjectAssignmentRequiredError("One or more projects are not assigned to current manager")
            if not AssignmentRepository.are_users_managed_by(manager_id, data.user_ids, db):
                raise ManagedUserRequiredError()

        AssignmentRepository.deassign_projects(data.user_ids, data.project_ids, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Projects successfully deassigned")

    @staticmethod
    def assign_roles(
        data: AssignmentSchema.RoleAssignmentRequest,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        if not UserRepository.are_users_present(data.user_ids, db):
            raise UserNotFoundError("One or more users not found")
        AssignmentRepository.assign_roles(data.user_ids, data.roles, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Roles successfully assigned")

    @staticmethod
    def deassign_roles(
        data: AssignmentSchema.RoleAssignmentRequest,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        if not UserRepository.are_users_present(data.user_ids, db):
            raise UserNotFoundError("One or more users not found")
        AssignmentRepository.deassign_roles(data.user_ids, data.roles, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Roles successfully deassigned")

    @staticmethod
    def sync_users_to_project(
        project_id: int,
        data: AssignmentSchema.AssignUsersToProjectRequest,
        current_user: dict,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        if ProjectRepository.get_project_by_id(project_id, db) is None:
            raise ProjectNotFoundError()
        if not UserRepository.are_users_present(data.user_ids, db):
            raise UserNotFoundError("One or more users not found")

        if "admin" not in current_user.get("user_roles", []):
            manager_id = current_user["user_id"]
            if not ProjectRepository.is_assigned([project_id], manager_id, db):
                raise ProjectAssignmentRequiredError("Project is not assigned to current manager")
            if not AssignmentRepository.are_users_managed_by(manager_id, data.user_ids, db):
                raise ManagedUserRequiredError()

        AssignmentRepository.sync_users_to_project(project_id, data.user_ids, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Users successfully synced to project")

    @staticmethod
    def sync_projects_to_user(
        user_id: int,
        data: AssignmentSchema.AssignProjectsToUserRequest,
        current_user: dict,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        if UserRepository.get_user_by_id(user_id, db) is None:
            raise UserNotFoundError()
        if not ProjectRepository.are_projects_present(data.project_ids, db):
            raise ProjectNotFoundError("One or more projects not found")

        if "admin" not in current_user.get("user_roles", []):
            manager_id = current_user["user_id"]
            if not AssignmentRepository.are_users_managed_by(manager_id, [user_id], db):
                raise ManagedUserRequiredError("User does not belong to current manager")
            if not ProjectRepository.is_assigned(data.project_ids, manager_id, db):
                raise ProjectAssignmentRequiredError("One or more projects are not assigned to current manager")

        AssignmentRepository.sync_projects_to_user(user_id, data.project_ids, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Projects successfully synced to user")

    @staticmethod
    def sync_roles_to_user(
        user_id: int,
        data: AssignmentSchema.AssignRolesToUserRequest,
        db: Session,
    ) -> AssignmentSchema.AssignmentMessageResponse:
        if UserRepository.get_user_by_id(user_id, db) is None:
            raise UserNotFoundError()
        AssignmentRepository.sync_roles_to_user(user_id, data.roles, db)
        return AssignmentSchema.AssignmentMessageResponse(message="Roles successfully synced to user")

