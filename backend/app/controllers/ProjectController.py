from app.schemas.UserSchema import UserResponse
from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from datetime import date

from app.dependencies.auth import get_current_user
from app.db.database import get_db
from app.models.RoleModel import RoleEnum as RE
from sqlalchemy.orm import Session

from app.models.ProjectModel import StatusEnum

from app.utils.RoleValidation import RoleValidation
import app.schemas.ProjectSchema as ProjectSchema
from app.services.ProjectService import ProjectService
from app.core.exceptions import AccessDeniedError, ArchivedProjectModificationError
from app.repositories.AssignmentRepository import AssignmentRepository
from app.repositories.ProjectRepository import ProjectRepository

router = APIRouter(prefix="/projects")


@router.post("", 
    response_model=ProjectSchema.ProjectResponse, 
    status_code=status.HTTP_201_CREATED
)
def create_project(
    data: ProjectSchema.ProjectCreateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN])
    return ProjectService.create_project(data, db)


@router.delete("/{project_id}", response_model=ProjectSchema.ProjectResponse)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN])
    return ProjectService.soft_delete_project(project_id, db)


@router.patch("/{project_id}", response_model=ProjectSchema.ProjectResponse)
def update_project(
    project_id: int,
    data: ProjectSchema.ProjectUpdateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN, RE.MANAGER])
    if not RE.ADMIN in current_user[ "user_roles" ] and not ProjectRepository.are_projects_assigned([project_id], current_user.get("user_id"), db):
        raise AccessDeniedError("You are not assigned to this project")

    if not RE.ADMIN in current_user[ "user_roles" ] and data.status == StatusEnum.ARCHIVED:
        raise ArchivedProjectModificationError("You are not allowed to archive this project")
    return ProjectService.update_project(project_id, data, current_user, db)


@router.get("/user/{user_id}", response_model=List[ProjectSchema.ProjectResponse])
def get_user_projects(
    user_id: int,
    sort_by: Optional[str] = Query(default="duration"),
    sort_type: int = Query(default=-1),
    status: Optional[List[str]] = Query(default=["in_progress"]),
    page: int | None = Query( default = None ),
    page_size: int | None = Query( default = None ),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN, RE.MANAGER, RE.EMPLOYEE])
    if RE.ADMIN in current_user.get("user_roles", []):
        pass
    elif user_id == current_user.get("user_id"):
        pass
    elif RE.MANAGER in current_user.get("user_roles", []):
        if not AssignmentRepository.can_view_users_projects(current_user.get("user_id"), [user_id], db):
            raise AccessDeniedError("You cannot view projects of this user")
    else:
        raise AccessDeniedError("Insufficient role")
    return ProjectService.get_projects(
        sort_by=sort_by,
        sort_type=sort_type,
        status_filters=status,
        current_user=current_user,
        user_id=user_id,
        page_size = page_size,
        page = page,
        db=db,
    )


@router.get("/{project_id}", response_model=ProjectSchema.ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN, RE.MANAGER, RE.EMPLOYEE])
    if not RE.ADMIN in current_user[ "user_roles" ] and not ProjectRepository.are_projects_assigned([project_id], current_user.get("user_id"), db):
        raise AccessDeniedError("You are not assigned to this project")
    return ProjectService.get_project_by_id(project_id, db)

@router.get("", response_model=List[ProjectSchema.ProjectResponse])
def get_projects(
    sort_by: Optional[str] = Query(default="duration"),
    sort_type: int = Query(default=-1),
    status: Optional[List[str]] = Query(default=["in_progress"]),
    page: int | None = Query( default = None),
    page_size: int | None = Query( default = None ),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN, RE.MANAGER, RE.EMPLOYEE])
    if RE.ADMIN in current_user.get("user_roles", []):
        return ProjectService.get_projects(
            sort_by=sort_by,
            sort_type=sort_type,
            status_filters=status,
            current_user=current_user,
            page_size = page_size,
            page = page,
            db=db,
        )
    return ProjectService.get_projects(
        sort_by=sort_by,
        sort_type=sort_type,
        status_filters=status,
        current_user=current_user,
        user_id=current_user[ "user_id" ],
        page = page,
        page_size = page_size,
        db = db
    )

@router.get( "/{project_id}/unassigned/users", response_model=List[UserResponse])
def get_project_unassigned_users( 
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    page: int | None = Query( default = None),
    page_size: int | None = Query( default = None )
):
    RoleValidation.validate_role(current_user, [RE.ADMIN, RE.MANAGER])
    return ProjectService.get_project_unassigned_users(project_id, current_user, db, page, page_size)