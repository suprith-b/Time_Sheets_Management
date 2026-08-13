from app.utils.InputValidation import InputValidation
from typing import List

from app.models.RoleModel import RoleEnum as RE
import app.schemas.TaskSchema as TaskSchema
from app.repositories.TaskRepository import TaskRepository
from app.repositories.ProjectRepository import ProjectRepository
from app.core.exceptions import AccessDeniedError, ProjectNotFoundError, TaskNotFoundError


class TaskService:

    @staticmethod
    def create_task(
        project_id: int,
        data: TaskSchema.TaskCreateRequest,
        current_user: dict,
        db,
    ) -> TaskSchema.TaskResponse:
        if ProjectRepository.get_project_by_id(project_id, db) is None:
            raise ProjectNotFoundError()

        if RE.ADMIN not in current_user.get("user_roles", []):
            assigned = ProjectRepository.are_projects_assigned(
                [project_id], current_user["user_id"], db
            )
            if not assigned:
                raise AccessDeniedError("Manager not assigned to this project")

        InputValidation.validate_length( "task name", data.name, 100 )
        InputValidation.validate_length( "task description", data.description, 300 )
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
            raise TaskNotFoundError()
        if RE.MANAGER in current_user.get("user_roles", []):
            assigned = ProjectRepository.are_projects_assigned(
                [task.project_id], current_user["user_id"], db
            )
            if not assigned:
                raise AccessDeniedError("Manager not assigned to this project")

        if data.name:
            InputValidation.validate_length( "task name", data.name, 100 )
        if data.description:
            InputValidation.validate_length( "task description", data.description, 300 )

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
            raise TaskNotFoundError()
        if RE.ADMIN not in current_user.get("user_roles", []):
            assigned = ProjectRepository.are_projects_assigned(
                [task.project_id], current_user["user_id"], db
            )
            if not assigned:
                raise AccessDeniedError("Manager not assigned to this project")
        deleted_task = TaskRepository.soft_delete_task(task, db)
        return TaskSchema.TaskResponse(**deleted_task.__dict__)

    @staticmethod
    def get_tasks(
        project_id: int,
        is_alive: List[int],
        current_user: dict,
        page: int | None,
        page_size: int | None,
        db,
    ) -> List[TaskSchema.TaskResponse]:
        bool_filters = [bool(v) for v in is_alive]
        tasks = TaskRepository.get_tasks(
            project_id=project_id,
            is_alive_filters=bool_filters,
            current_user=current_user,
            page = page,
            page_size = page_size,
            db=db,
        )
        return [TaskSchema.TaskResponse(**t.__dict__) for t in tasks]
