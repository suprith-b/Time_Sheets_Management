from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from datetime import date

from app.dependencies.auth import get_current_user
from app.db.database import get_db
from sqlalchemy.orm import Session

from app.utils.RoleValidation import RoleValidation
import app.schemas.ProjectSchema as ProjectSchema
from app.services.ProjectService import ProjectService

router = APIRouter(prefix="/projects")


@router.post("", 
            response_model=ProjectSchema.ProjectResponse, 
            status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectSchema.ProjectCreateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin"])
    return ProjectService.create_project(data, db)


@router.delete("/{project_id}", response_model=ProjectSchema.ProjectResponse)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin"])
    return ProjectService.soft_delete_project(project_id, db)


@router.patch("/{project_id}", response_model=ProjectSchema.ProjectResponse)
def update_project(
    project_id: int,
    data: ProjectSchema.ProjectUpdateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin", "manager"])
    return ProjectService.update_project(project_id, data, current_user, db)


@router.get("/{user_id}", response_model=List[ProjectSchema.ProjectResponse])
def list_projects(
    user_id: int,
    sort_by: Optional[str] = Query(default="duration"),
    sort_type: int = Query(default=-1),
    status: Optional[List[str]] = Query(default=["in_progress"]),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return ProjectService.get_projects(
        user_id=user_id,
        sort_by=sort_by,
        sort_type=sort_type,
        status_filters=status,
        current_user=current_user,
        db=db,
    )

@router.get("", response_model=List[ProjectSchema.ProjectResponse])
def get_projects(
    sort_by: Optional[str] = Query(default="duration"),
    sort_type: int = Query(default=-1),
    status: Optional[List[str]] = Query(default=["in_progress"]),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin"])
    return ProjectService.get_all_projects(
        sort_by=sort_by,
        sort_type=sort_type,
        status_filters=status,
        current_user=current_user,
        db=db,
    )
