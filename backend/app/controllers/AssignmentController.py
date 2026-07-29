from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
import app.schemas.AssignmentSchema as AssignmentSchema
from app.services.AssignmentService import AssignmentService
from app.utils.RoleValidation import RoleValidation

router = APIRouter(prefix="/assignments")


@router.put(
    "/users/to/manager/{manager_id}",
    response_model=AssignmentSchema.AssignmentMessageResponse
)
def assign_users_to_manager(
    manager_id: int,
    data: AssignmentSchema.AssignUsersToManagerRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin"])
    return AssignmentService.assign_users_to_manager(manager_id, data, db)


@router.post(
    "/projects/assign",
    response_model=AssignmentSchema.AssignmentMessageResponse
)
def assign_projects(
    data: AssignmentSchema.ProjectAssignmentRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin", "manager"])
    return AssignmentService.assign_projects(data, current_user, db)


@router.patch("/projects/deassign", response_model=AssignmentSchema.AssignmentMessageResponse)
def deassign_projects(
    data: AssignmentSchema.ProjectAssignmentRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin", "manager"])
    return AssignmentService.deassign_projects(data, current_user, db)


@router.post("/roles/assign", response_model=AssignmentSchema.AssignmentMessageResponse)
def assign_roles(
    data: AssignmentSchema.RoleAssignmentRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin"])
    return AssignmentService.assign_roles(data, db)


@router.patch("/roles/deassign", response_model=AssignmentSchema.AssignmentMessageResponse)
def deassign_roles(
    data: AssignmentSchema.RoleAssignmentRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin"])
    return AssignmentService.deassign_roles(data, db)


@router.post(
    "/users/to/project/{project_id}",
    response_model=AssignmentSchema.AssignmentMessageResponse,
)
def sync_users_to_project(
    project_id: int,
    data: AssignmentSchema.AssignUsersToProjectRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin", "manager"])
    return AssignmentService.sync_users_to_project(project_id, data, current_user, db)


@router.post(
    "/projects/to/user/{user_id}",
    response_model=AssignmentSchema.AssignmentMessageResponse,
)
def sync_projects_to_user(
    user_id: int,
    data: AssignmentSchema.AssignProjectsToUserRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin", "manager"])
    return AssignmentService.sync_projects_to_user(user_id, data, current_user, db)


@router.post(
    "/roles/to/user/{user_id}",
    response_model=AssignmentSchema.AssignmentMessageResponse,
)
def sync_roles_to_user(
    user_id: int,
    data: AssignmentSchema.AssignRolesToUserRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin"])
    return AssignmentService.sync_roles_to_user(user_id, data, db)

