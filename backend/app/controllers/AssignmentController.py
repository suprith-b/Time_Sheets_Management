from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.RoleModel import RoleEnum as RE
import app.schemas.AssignmentSchema as AssignmentSchema
from app.services.AssignmentService import AssignmentService
from app.utils.RoleValidation import RoleValidation
from app.core.exceptions import AccessDeniedError, ManagedUserRequiredError, ProjectAssignmentRequiredError, UserNotFoundError
from app.repositories.AssignmentRepository import AssignmentRepository
from app.repositories.ProjectRepository import ProjectRepository
from app.repositories.UserRepository import UserRepository

router = APIRouter(prefix="/assignments")

@router.post("/roles/add", status_code=status.HTTP_200_OK)
def add_roles_to_users(
    data: AssignmentSchema.UsersRoleAssignmentRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN])
    AssignmentService.add_roles_to_users(data.users, data.roles, db)
    return {"users": data.users, "roles": [role.value for role in data.roles]}


@router.patch("/roles/revoke", status_code=status.HTTP_200_OK)
def revoke_roles_from_users(
    data: AssignmentSchema.UsersRoleAssignmentRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN])
    AssignmentService.revoke_roles_from_users(data.users, data.roles, db)
    return {"users": data.users, "roles": [role.value for role in data.roles]}


@router.patch("/manager/{manager_id}", status_code=status.HTTP_200_OK)
def update_manager_for_users(
    manager_id: int,
    data: AssignmentSchema.UserListRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN])
    AssignmentService.assign_manager(manager_id, data.users, db)
    return {"manager_id": manager_id, "users": data.users}


@router.post("/projects/add/to/user/{user_id}", status_code=status.HTTP_200_OK)
def add_projects_to_user(
    user_id: int,
    data: AssignmentSchema.ProjectAssignmentRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN, RE.MANAGER])
    if not RE.ADMIN in current_user.get("user_roles", []):
        if not AssignmentRepository.are_users_managed_by(current_user.get("user_id"), [user_id], db):
            raise AccessDeniedError("You cannot assign projects to a user you do not manage.")
        
        if not ProjectRepository.are_projects_assigned(data.projects, current_user.get("user_id"), db):
            raise AccessDeniedError("You are not assigned to one or more specified projects.")
        
    AssignmentService.add_projects_to_user(user_id, data.projects, current_user, db)
    return {"user_id": user_id, "projects": data.projects}

@router.post("/projects/revoke/from/user/{user_id}", status_code=status.HTTP_200_OK)
def revoke_projects_from_user(
    user_id: int,
    data: AssignmentSchema.ProjectAssignmentRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN, RE.MANAGER])
    if not RE.ADMIN in current_user.get("user_roles", []):
        if not AssignmentRepository.can_view_users_projects(current_user.get("user_id"), [user_id], db):
            raise AccessDeniedError("You cannot revoke projects from a user you do not manage.")
        
        if not ProjectRepository.are_projects_assigned(data.projects, current_user.get("user_id"), db):
            raise AccessDeniedError("You are not assigned to one or more specified projects.")
        
    AssignmentService.revoke_projects_from_user(user_id, data.projects, current_user, db)
    return {"user_id": user_id, "projects": data.projects}


@router.post("/users/add/to/project/{project_id}", status_code=status.HTTP_200_OK)
def add_users_to_project(
    project_id: int,
    data: AssignmentSchema.ProjectUserAssignmentRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN, RE.MANAGER])

    if not UserRepository.check_users_role([data.users], RE.EMPLOYEE, db):
        raise UserNotFoundError("One or more users are not employees")
    
    if not RE.ADMIN in current_user.get("user_roles", []):
        if not ProjectRepository.are_projects_assigned([project_id], current_user.get("user_id"), db):
            raise ProjectAssignmentRequiredError("You are not assigned to the specified project.")

        if not UserRepository.are_users_managed_by(current_user.get("user_id"), data.users, db):
            raise ManagedUserRequiredError("You do not manage one or more of the specified users")

    AssignmentService.add_users_to_project(project_id, data.users, current_user, db)
    return {"project_id": project_id, "users": data.users}

@router.post("/users/revoke/from/project/{project_id}", status_code=status.HTTP_200_OK)
def revoke_users_from_project(
    project_id: int,
    data: AssignmentSchema.ProjectUserAssignmentRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN, RE.MANAGER])

    if not RE.ADMIN in current_user.get("user_roles", []):
        if not ProjectRepository.are_projects_assigned([project_id], current_user.get("user_id"), db):
            raise ProjectAssignmentRequiredError("You are not assigned to the specified project.")
        
    AssignmentService.revoke_users_from_project(project_id, data.users, current_user, db)
    return {"project_id": project_id, "users": data.users}

