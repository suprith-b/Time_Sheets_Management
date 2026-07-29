from fastapi import HTTPException, status
from typing import List

import app.schemas.TaskSchema as TaskSchema
from app.repositories.TaskRepository import TaskRepository
from app.repositories.ProjectRepository import ProjectRepository


class TaskService:

    @staticmethod
    def create_task(
        project_id: int,
        data: TaskSchema.TaskCreateRequest,
        current_user: dict,
        db,
    ) -> TaskSchema.TaskResponse:

        if "admin" not in current_user.get("user_roles", []):
            assigned = ProjectRepository.is_assigned(
                [project_id], current_user["user_id"], db
            )
            if not assigned:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Manager not assigned to this project",
                )

        task = TaskRepository.create_task(project_id, data, db)
        return TaskSchema.TaskResponse(**task.__dict__)

    @staticmethod
    def update_task(
        task_id: int,
        data: TaskSchema.TaskUpdateRequest,
        current_user: dict,
        db,
    ) -> TaskSchema.TaskResponse:
        
        task = TaskRepository.get_task(task_id, db)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        if "manager" in current_user.get("user_roles", []):
            assigned = ProjectRepository.is_assigned(
                [task.project_id], current_user["user_id"], db
            )
            if not assigned:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Manager not assigned to this project",
                )
        updates = data.model_dump(exclude_none=True)
        updated_task = TaskRepository.update_task(task, updates, db)
        return TaskSchema.TaskResponse(**updated_task.__dict__)

    @staticmethod
    def delete_task(
        task_id: int,
        current_user: dict,
        db,
    ) -> TaskSchema.TaskResponse:
        
        task = TaskRepository.get_task(task_id, db)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        if "admin" not in current_user.get("user_roles", []):
            assigned = ProjectRepository.is_assigned(
                [task.project_id], current_user["user_id"], db
            )
            if not assigned:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Manager not assigned to this project",
                )
        deleted_task = TaskRepository.soft_delete_task(task, db)
        return TaskSchema.TaskResponse(**deleted_task.__dict__)

    @staticmethod
    def get_tasks(
        project_id: int,
        is_alive: List[int],
        current_user: dict,
        db,
    ) -> List[TaskSchema.TaskResponse]:
        bool_filters = [bool(v) for v in is_alive]
        tasks = TaskRepository.get_tasks(
            project_id=project_id,
            is_alive_filters=bool_filters,
            current_user=current_user,
            db=db,
        )
        return [TaskSchema.TaskResponse(**t.__dict__) for t in tasks]
