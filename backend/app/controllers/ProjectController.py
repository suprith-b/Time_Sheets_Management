from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user

from app.db.database import get_db
from app.dependencies.auth import get_current_user
import app.schemas.ProjectSchema as ProjectSchema
from app.services.ProjectService import ProjectService


router = APIRouter(prefix="/projects")


@router.get("")
def get_projects(
	db: Session = Depends(get_db),
	current_user: dict = Depends(get_current_user),
):
	return ProjectService.get_projects(current_user, db)


@router.post("")
def create_project(
	data: ProjectSchema.CreateProject,
	db: Session = Depends(get_db),
	current_user: dict = Depends(get_current_user),
):
	if current_user["user_role"] != "admin":
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="You do not have permission to access this resource",
		)
	return ProjectService.create_project(data, db)


@router.delete("/{project_id}")
def delete_project(
	project_id: int,
	db: Session = Depends(get_db),
	current_user: dict = Depends(get_current_user),
):
	if current_user["user_role"] != "admin":
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="You do not have permission to access this resource",
		)
	return ProjectService.delete_project(project_id, db)


@router.patch("/{project_id}")
def edit_project(
	project_id: int,
	data: ProjectSchema.EditProject,
	db: Session = Depends(get_db),
	current_user: dict = Depends(get_current_user),
):
	if current_user["user_role"] not in {"admin", "manager"}:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="You do not have permission to access this resource",
		)
	return ProjectService.edit_project(project_id, data, current_user, db)
