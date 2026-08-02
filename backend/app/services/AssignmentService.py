from sqlalchemy.orm import Session

from app.core.exceptions import (
    AccessDeniedError,
    ManagerNotFoundError,
    ManagedUserRequiredError,
    ProjectAssignmentRequiredError,
    ProjectNotFoundError,
    UserNotFoundError,
)
from app.models.ProjectAssignmentModel import ProjectAssignment
from app.models.RoleModel import RoleEnum as RE
from app.models.UserModel import User
from app.repositories.AssignmentRepository import AssignmentRepository
from app.repositories.ProjectRepository import ProjectRepository
from app.repositories.UserRepository import UserRepository


class AssignmentService:

    @staticmethod
    def add_roles_to_users(users: list[int], roles: list[RE], db: Session) -> None:
        if not users or not roles:
            return
        if not UserRepository.are_users_present(users, db):
            raise UserNotFoundError()

        AssignmentRepository.add_user_roles(users, roles, db)

    @staticmethod
    def revoke_roles_from_users(users: list[int], roles: list[RE], db: Session) -> None:
        if not users or not roles:
            return
        if not UserRepository.are_users_present(users, db):
            raise UserNotFoundError()

        AssignmentRepository.revoke_users_roles(users, roles, db)

    @staticmethod
    def assign_manager(manager_id: int, users: list[int], db: Session) -> None:
        if not UserRepository.are_users_present(users, db):
            raise UserNotFoundError()
        if not UserRepository.check_users_role([manager_id], RE.MANAGER, db):
            raise ManagerNotFoundError()
        if not UserRepository.check_users_role(users, RE.EMPLOYEE, db):
            raise AccessDeniedError("One or more users are not employees")

        db.query(User).filter(User.id.in_(users)).update({User.manager_id: manager_id}, synchronize_session=False)
        db.commit()

    @staticmethod
    def add_projects_to_user(user_id: int, projects: list[int], current_user: dict, db: Session) -> None:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise UserNotFoundError()
        if not ProjectRepository.are_projects_present(projects, db):
            raise ProjectNotFoundError()

        if not RE.ADMIN in current_user[ "user_roles" ]:
            if not ProjectRepository.are_projects_assigned(projects, current_user["user_id"], db):
                raise ProjectAssignmentRequiredError()
            if not user.manager_id == current_user["user_id"]:
                raise ManagedUserRequiredError("You are not the manager of this user")

        AssignmentRepository.add_projects_to_user(user_id, projects, current_user, db)

    @staticmethod
    def revoke_projects_from_user(user_id: int, projects: list[int], current_user: dict, db: Session) -> None:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise UserNotFoundError()
        
        if not ProjectRepository.are_projects_present(projects, db):
            raise ProjectNotFoundError()

        if not RE.ADMIN in current_user[ "user_roles" ]:
            if not ProjectRepository.are_projects_assigned(projects, current_user["user_id"], db):
                raise ProjectAssignmentRequiredError()
            if not AssignmentRepository.can_view_users_projects(current_user.get("user_id"), [user_id], db):
                raise ManagedUserRequiredError("You cannot revoke projects from a user you do not manage")

        AssignmentRepository.revoke_projects_from_user(user_id, projects, current_user, db)


    @staticmethod
    def add_users_to_project(project_id: int, users: list[int], current_user: dict, db: Session) -> None:
        if ProjectRepository.get_project_by_id(project_id, db) is None:
            raise ProjectNotFoundError()
        
        if not UserRepository.are_users_present(users, db):
            raise UserNotFoundError()

        AssignmentRepository.add_users_to_project(project_id, users, db)

    @staticmethod
    def revoke_users_from_project(project_id: int, users: list[int], current_user: dict, db: Session) -> None:
        if ProjectRepository.get_project_by_id(project_id, db) is None:
            raise ProjectNotFoundError()
        if not UserRepository.are_users_present(users, db):
            raise UserNotFoundError()
        
        AssignmentRepository.revoke_users_from_project(project_id, users, db)