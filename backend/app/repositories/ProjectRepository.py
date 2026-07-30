from typing import Optional
from sqlalchemy.orm import Session

from app.models.ProjectModel import Project, StatusEnum
import app.schemas.ProjectSchema as ProjectSchema
from app.models.ProjectAssignmentModel import ProjectAssignment

class ProjectRepository:

    @staticmethod
    def get_user_projects(user_id: int, db: Session) -> list[Project]:
        return (
            db.query(Project)
            .join(ProjectAssignment, Project.id == ProjectAssignment.project_id)
            .filter(
                ProjectAssignment.user_id == user_id,
                ProjectAssignment.is_assigned.is_(True),
            )
            .all()
        )

    @staticmethod
    def is_assigned(project_ids: list[int], user_id: int, db: Session) -> bool:
        return db.query(ProjectAssignment).filter(
            ProjectAssignment.project_id.in_(project_ids), 
            ProjectAssignment.user_id == user_id
        ).count() == len(project_ids)

    @staticmethod
    def are_projects_present(project_ids: list[int], db: Session) -> bool:
        return db.query(Project.id).filter(Project.id.in_(project_ids)).count() == len(set(project_ids))


    @staticmethod
    def create_project(data: ProjectSchema.ProjectCreateRequest, db: Session) -> Project:
        
        project = Project(
            name=data.name,
            status=data.status,
            duration=data.duration,
            start_date=data.start_date,
            end_date=data.end_date,
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def get_project_by_id(project_id: int, db: Session) -> Project | None:
        return db.query(Project).filter(Project.id == project_id).first()

    @staticmethod
    def soft_delete_project(project_id: int, db: Session) -> Project | None:
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            project.status = StatusEnum.ARCHIVED
            db.commit()
            db.refresh(project)
        return project

    @staticmethod
    def update_project(project: Project, data: dict, db: Session) -> Project | None:
        for field, value in data.model_dump(exclude_none=True).items():
            if hasattr(project, field):
                setattr(project, field, value)
        
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def get_projects(
        sort_by: str,
        sort_type: int,
        status_filters: list[StatusEnum],
        db: Session,
        user_id: Optional[int] = None
    ) -> list[Project] | None:
        query = (
            db.query(Project).filter(
                Project.status.in_(status_filters),
            )
        )
        if user_id:
            query = query.join(
                ProjectAssignment,
                Project.id == ProjectAssignment.project_id
            ).filter(
                ProjectAssignment.user_id == user_id, 
                ProjectAssignment.is_assigned
            )
        
        sort_column = getattr(Project, sort_by, Project.duration)
        if sort_type == -1:
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
        return query.all()

