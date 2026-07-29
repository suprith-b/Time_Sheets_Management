from sqlalchemy.orm import Session
from starlette import status
from fastapi import HTTPException
from datetime import date, timedelta
from typing import List

from app.models.ProjectModel import StatusEnum
from app.repositories.ProjectRepository import ProjectRepository
import app.schemas.ProjectSchema as ProjectSchema
from app.repositories.AssignmentRepository import AssignmentRepository

class ProjectService:

    @staticmethod
    def create_project(data: ProjectSchema.ProjectCreateRequest, db) -> ProjectSchema.ProjectResponse:
        
        data.status = data.status or StatusEnum.CREATED
        if data.status == StatusEnum.IN_PROGRESS:
            data.start_date = date.today()
            data.end_date = data.start_date + timedelta(days=data.duration)

        project = ProjectRepository.create_project(data, db)
        return ProjectSchema.ProjectResponse(**project.__dict__)

    @staticmethod
    def soft_delete_project(project_id: int, db: Session) -> ProjectSchema.ProjectResponse:
        project = ProjectRepository.soft_delete_project(project_id, db)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Project not found"
            )
        return ProjectSchema.ProjectResponse(**project.__dict__)

    @staticmethod
    def update_project(project_id: int, data: ProjectSchema.ProjectUpdateRequest, current_user: dict, db: Session) -> ProjectSchema.ProjectResponse:
        
        project = ProjectRepository.get_project_by_id( project_id, db )
        if project is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Project not found"
            )

        is_admin = "admin" in current_user.get("user_roles", [])
        is_manager = "manager" in current_user.get("user_roles", [])

        if not is_admin and not is_manager:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")

        if is_manager and project.status == StatusEnum.ARCHIVED:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Managers cannot modify archived projects")

        changed_fields = data.model_dump( exclude_none=True )

        if not is_admin and len( set( changed_fields ).union( { "end_date", "status", "duration" } ) ) > 3:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "One or more fields cannot be changed by manager"
            )

        if data.status is not None and project.start_date is None:
            data.start_date = date.today()
            data.end_date = data.start_date + timedelta(days=project.duration)

        if data.duration and data.end_date:
            data.end_date = None
        
        data = ProjectRepository.update_project(project, data, db)
        return ProjectSchema.ProjectResponse(**data.__dict__)

    @staticmethod
    def get_projects(
        user_id: int,
        sort_by: str,
        sort_type: int,
        status_filters: List[str],
        current_user: dict,
        db: Session,
    ) -> List[ProjectSchema.ProjectResponse]:
        user_roles = current_user.get("user_roles", [])
        current_user_id = current_user.get("user_id")

        if "admin" in user_roles:
            pass
        elif current_user_id == user_id:
            pass
        elif "manager" in user_roles:

            if not AssignmentRepository.are_users_managed_by(current_user_id, [user_id], db):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to this resource",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        status_list = [StatusEnum(s) for s in status_filters]
        projects = ProjectRepository.get_projects(
            user_id=user_id,
            sort_by=sort_by,
            sort_type=sort_type,
            status_filters=status_list,
            db=db,
        )
        return [ProjectSchema.ProjectResponse(**p.__dict__) for p in projects]

    @staticmethod
    def get_all_projects(
        sort_by: str,
        sort_type: int,
        status_filters: List[str],
        current_user: dict,
        db: Session,
    ) -> List[ProjectSchema.ProjectResponse]:
        
        status_list = [StatusEnum(s) for s in status_filters]
        projects = ProjectRepository.get_projects(
            sort_by=sort_by,
            sort_type=sort_type,
            status_filters=status_list,
            db=db,
        )
        return [ProjectSchema.ProjectResponse(**p.__dict__) for p in projects]

