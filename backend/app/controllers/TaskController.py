from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional

from app.dependencies.auth import get_current_user
from app.models.RoleModel import RoleEnum as RE
from app.db.database import get_db
from sqlalchemy.orm import Session

from app.utils.RoleValidation import RoleValidation
import app.schemas.TaskSchema as TaskSchema
from app.services.TaskService import TaskService

router = APIRouter(prefix="/tasks")

@router.post(
    "/{project_id}",
    response_model=TaskSchema.TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    project_id: int,
    data: TaskSchema.TaskCreateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN, RE.MANAGER])
    return TaskService.create_task(project_id, data, current_user, db)

@router.patch(
    "/{task_id}",
    response_model=TaskSchema.TaskResponse,
)
def update_task(
    task_id: int,
    data: TaskSchema.TaskUpdateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN, RE.MANAGER])
    return TaskService.update_task(task_id, data, current_user, db)

@router.delete(
    "/{task_id}",
    response_model=TaskSchema.TaskResponse,
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN, RE.MANAGER])
    return TaskService.delete_task(task_id, current_user, db)

@router.get(
    "/{project_id}",
    response_model=List[TaskSchema.TaskResponse],
)
def get_tasks(
    project_id: int,
    is_alive: Optional[List[int]] = Query(default=[1]),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    page: int | None = Query( default = None ),
    page_size: int | None = Query( default = None ),
):
    return TaskService.get_tasks(
        project_id=project_id,
        is_alive=is_alive,
        current_user=current_user,
        page = page,
        page_size = page_size,
        db=db,
    )
