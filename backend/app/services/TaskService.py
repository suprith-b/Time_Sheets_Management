from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import app.schemas.TaskSchema as TaskSchema
from app.repositories.ProjectRepository import ProjectRepository
from app.repositories.TaskRepository import TaskRepository


class TaskService:
    @staticmethod
    def _check_project_access(
        project_id: int,
        current_user: dict,
        db: Session,
    ):
        if ProjectRepository.get_project_by_id(project_id, db) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        if current_user["user_role"] != "admin" and not ProjectRepository.is_user_assigned(
            project_id,
            current_user["user_id"],
            db,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this project",
            )

    @staticmethod
    def get_tasks(project_id: int, current_user: dict, db: Session):
        TaskService._check_project_access(project_id, current_user, db)
        tasks = TaskRepository.get_tasks_by_project(project_id, db)
        return [TaskSchema.TaskResponse.model_validate(task) for task in tasks]

    @staticmethod
    def create_task(
        project_id: int,
        data: TaskSchema.CreateTask,
        current_user: dict,
        db: Session,
    ):
        TaskService._check_project_access(project_id, current_user, db)
        task = TaskRepository.create_task(project_id, data, db)
        return TaskSchema.TaskResponse.model_validate(task)

    @staticmethod
    def edit_task(
        task_id: int,
        data: TaskSchema.EditTask,
        current_user: dict,
        db: Session,
    ):
        task = TaskRepository.get_task_by_id(task_id, db)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        TaskService._check_project_access(task.project_id, current_user, db)
        task = TaskRepository.edit_task(task_id, data, db)
        return TaskSchema.TaskResponse.model_validate(task)

    @staticmethod
    def delete_task(task_id: int, current_user: dict, db: Session):
        task = TaskRepository.get_task_by_id(task_id, db)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        TaskService._check_project_access(task.project_id, current_user, db)
        task = TaskRepository.delete_task(task_id, db)
        return TaskSchema.TaskResponse.model_validate(task)
