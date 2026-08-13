from app.utils.InputValidation import InputValidation
from sqlalchemy.sql.functions import current_user
from app.repositories.UserRepository import UserRepository
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List, Optional

from app.models.ProjectModel import StatusEnum
from app.models.RoleModel import RoleEnum as RE
from app.repositories.ProjectRepository import ProjectRepository
from app.repositories.TaskRepository import TaskRepository
import app.schemas.ProjectSchema as ProjectSchema
import app.schemas.UserSchema as UserSchema
from app.repositories.AssignmentRepository import AssignmentRepository
from app.core.exceptions import AccessDeniedError, ArchivedProjectModificationError, InvalidDateRangeError, ProjectFieldUpdateForbiddenError, ProjectNotFoundError

class ProjectService:

    @staticmethod
    def get_project_unassigned_users(
        project_id: int,
        current_user: dict,
        db: Session,
        page: int | None,
        page_size: int | None
    ) -> List[UserSchema.UserResponse]:
        project = ProjectRepository.get_project_by_id( project_id, db )
        if not project:
            raise ProjectNotFoundError()

        assigned_users = [ u[ "id" ] for u in 
            UserRepository.get_users(
            db = db,
            manager_id = current_user[ "user_id" ] if RE.ADMIN not in current_user[ "user_roles" ] else None,
            is_alive = [ 1 ],
            project_ids = [ project_id ],
            has_manager = [ True, False ],
            current_user = current_user,
            page = page,
            page_size = page_size,
            roles = None,
            )
        ]

        unassigned_users = ProjectRepository.get_project_unassigned_users(
            project_id = project_id,
            current_user = current_user,
            assigned_users = assigned_users,
            page_size = page_size,
            page = page,
            db = db
            )
        return [UserSchema.UserResponse(**u.__dict__) for u in unassigned_users]
        
        
        

    @staticmethod
    def create_project(data: ProjectSchema.ProjectCreateRequest, db) -> ProjectSchema.ProjectResponse:
        
        data.status = data.status or StatusEnum.CREATED
        if data.status == StatusEnum.IN_PROGRESS:
            data.start_date = date.today()
            data.end_date = data.start_date + timedelta(days=data.duration)

        if data.start_date and data.end_date and data.end_date < data.start_date:
            raise InvalidDateRangeError("End date cannot be earlier than start date")
        
        InputValidation.validate_length( "project name", data.name, 50 )

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
            data.end_date = None
        
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
        
        if data.name:
            InputValidation.validate_length( "project name", data.name, 50 )


        data = ProjectRepository.update_project(project, data, db)
        return ProjectSchema.ProjectResponse(**data.__dict__)

    @staticmethod
    def get_projects(
        sort_by: str,
        sort_type: int,
        status_filters: List[str],
        db: Session,
        current_user: dict,
        page: int | None,
        page_size: int | None,
        user_id: Optional[int] = None,
    ) -> List[ProjectSchema.ProjectResponse]:
        
        status_list = [StatusEnum(s) for s in status_filters]

        if user_id is not None:
            projects = ProjectRepository.get_projects(
                sort_by=sort_by,
                sort_type=sort_type,
                status_filters=status_list,
                user_id=user_id,
                page = page,
                page_size = page_size,
                db=db,
            )
        else:
            projects = ProjectRepository.get_projects(
                sort_by=sort_by,
                sort_type=sort_type,
                status_filters=status_list,
                page = page,
                page_size = page_size,
                db=db,
            )
        return [ProjectSchema.ProjectResponse(**p.__dict__, num_tasks=TaskRepository.get_task_count(p.id, db)) for p in projects]

    @staticmethod
    def get_project_by_id(project_id: int, db: Session) -> ProjectSchema.ProjectResponse:
        project = ProjectRepository.get_project_by_id(project_id, db)
        if not project:
            raise ProjectNotFoundError()
        return ProjectSchema.ProjectResponse(**project.__dict__)