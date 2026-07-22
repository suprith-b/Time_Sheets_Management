from sqlalchemy.orm import Session

from app.models.ProjectAssignmentModel import ProjectAssignment
from app.models.ProjectModel import Project


class ProjectAssignmentRepository:
    @staticmethod
    def assign_projects(user_id: int, project_ids: list[int], db: Session):
        db.query(ProjectAssignment).filter(
            ProjectAssignment.user_id == user_id
        ).delete(synchronize_session=False)

        db.add_all(
            ProjectAssignment(user_id=user_id, project_id=project_id)
            for project_id in project_ids
        )
        db.commit()