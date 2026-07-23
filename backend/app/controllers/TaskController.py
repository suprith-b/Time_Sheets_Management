from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.schemas.TaskSchema as TaskSchema
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.services.TaskService import TaskService


router = APIRouter(prefix="/task")


@router.get("/{project_id}")
def get_tasks(
	project_id: int,
	db: Session = Depends(get_db),
	current_user: dict = Depends(get_current_user),
):
	return TaskService.get_tasks(project_id, current_user, db)


@router.post("/{project_id}")
def create_task(
	project_id: int,
	data: TaskSchema.CreateTask,
	db: Session = Depends(get_db),
	current_user: dict = Depends(get_current_user),
):
	if current_user["user_role"] not in {"admin", "manager"}:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="You do not have permission to access this resource",
		)
	return TaskService.create_task(project_id, data, current_user, db)


@router.patch("/{task_id}")
def edit_task(
	task_id: int,
	data: TaskSchema.EditTask,
	db: Session = Depends(get_db),
	current_user: dict = Depends(get_current_user),
):
	if current_user["user_role"] not in {"admin", "manager"}:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="You do not have permission to access this resource",
		)
	return TaskService.edit_task(task_id, data, current_user, db)


@router.delete("/{task_id}")
def delete_task(
	task_id: int,
	db: Session = Depends(get_db),
	current_user: dict = Depends(get_current_user),
):
	if current_user["user_role"] not in {"admin", "manager"}:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="You do not have permission to access this resource",
		)
	return TaskService.delete_task(task_id, current_user, db)
