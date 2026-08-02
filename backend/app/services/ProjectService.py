from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List, Optional

from app.models.ProjectModel import StatusEnum
from app.models.RoleModel import RoleEnum as RE
from app.repositories.ProjectRepository import ProjectRepository
from app.repositories.TaskRepository import TaskRepository
import app.schemas.ProjectSchema as ProjectSchema
from app.repositories.AssignmentRepository import AssignmentRepository
from app.core.exceptions import AccessDeniedError, ArchivedProjectModificationError, InvalidDateRangeError, ProjectFieldUpdateForbiddenError, ProjectNotFoundError

class ProjectService:

    @staticmethod
    def create_project(data: ProjectSchema.ProjectCreateRequest, db) -> ProjectSchema.ProjectResponse:
        
        data.status = data.status or StatusEnum.CREATED
        if data.status == StatusEnum.IN_PROGRESS:
            data.start_date = date.today()
            data.end_date = data.start_date + timedelta(days=data.duration)

        if data.start_date and data.end_date and data.end_date < data.start_date:
            raise InvalidDateRangeError("End date cannot be earlier than start date")
        
        project = ProjectRepository.create_project(data, db)
        to_return = ProjectSchema.ProjectResponse(**project.__dict__)
        if data.tasks:
            TaskRepository.create_tasks(project.id, data.tasks, db)
        return to_return

    @staticmethod
    def soft_delete_project(project_id: int, db: Session) -> ProjectSchema.ProjectResponse:
        project = ProjectRepository.soft_delete_project(project_id, db)
        if not project:
            raise ProjectNotFoundError()
        return ProjectSchema.ProjectResponse(**project.__dict__)

    @staticmethod
    def update_project(project_id: int, data: ProjectSchema.ProjectUpdateRequest, current_user: dict, db: Session) -> ProjectSchema.ProjectResponse:

        if data.end_date:
            raise InvalidDateRangeError("End date cannot be updated directly. Update duration or start date instead.")
        
        project = ProjectRepository.get_project_by_id( project_id, db )
        if project is None:
            raise ProjectNotFoundError()

        is_admin = RE.ADMIN in current_user.get("user_roles", [])
        is_manager = RE.MANAGER in current_user.get("user_roles", [])

        if not is_admin and not is_manager:
            raise AccessDeniedError("Insufficient role")

        if not is_admin and project.status == StatusEnum.ARCHIVED:
            raise ArchivedProjectModificationError()

        changed_fields = data.model_dump( exclude_none=True )

        if not is_admin and len( set( changed_fields ).union( { "status", "duration" } ) ) > 3:
            raise ProjectFieldUpdateForbiddenError()

        if data.status is not None and project.start_date is None:
            data.start_date = date.today()

        effective_start_date = data.start_date or project.start_date
        if project.end_date and project.end_date < effective_start_date:
            raise InvalidDateRangeError("Start date cannot be later than end date")

        if data.duration is not None:
            data.end_date = effective_start_date + timedelta(days=data.duration)
        else:
            data.end_date = effective_start_date + timedelta(days=project.duration)
        
        data = ProjectRepository.update_project(project, data, db)
        return ProjectSchema.ProjectResponse(**data.__dict__)

    @staticmethod
    def get_projects(
        sort_by: str,
        sort_type: int,
        status_filters: List[str],
        current_user: dict,
        db: Session,
        user_id: Optional[int] = None,
    ) -> List[ProjectSchema.ProjectResponse]:
        
        status_list = [StatusEnum(s) for s in status_filters]
        manager_project_ids = []
        check_can_revoke = False
        if current_user.get("user_id") == user_id:
            pass
        elif RE.ADMIN not in current_user.get("user_roles", []):
            check_can_revoke = True
        if user_id is not None:
            manager_project_ids = [p.id for p in ProjectRepository.get_projects(
                sort_by=sort_by,
                sort_type=sort_type,
                status_filters=status_list,
                user_id=current_user.get("user_id"),
                db=db,
            )]
            projects = ProjectRepository.get_projects(
                sort_by=sort_by,
                sort_type=sort_type,
                status_filters=status_list,
                user_id=user_id,
                db=db,
            )
        else:
            projects = ProjectRepository.get_projects(
                sort_by=sort_by,
                sort_type=sort_type,
                status_filters=status_list,
                db=db,
            )
        
        return [ProjectSchema.ProjectResponse(**p.__dict__, can_revoke_project=(
            True if not check_can_revoke else p.id in manager_project_ids
        ), num_tasks=TaskRepository.get_task_count(p.id, db)) for p in projects]

    @staticmethod
    def get_project_by_id(project_id: int, db: Session) -> ProjectSchema.ProjectResponse:
        project = ProjectRepository.get_project_by_id(project_id, db)
        if not project:
            raise ProjectNotFoundError()
        return ProjectSchema.ProjectResponse(**project.__dict__)