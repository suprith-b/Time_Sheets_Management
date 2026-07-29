from sqlalchemy.orm import Session

from app.models.TaskModel import Task
from app.models.ProjectAssignmentModel import ProjectAssignment
import app.schemas.TaskSchema as TaskSchema

class TaskRepository:

    @staticmethod
    def create_task(
        project_id: int,
        data: TaskSchema.TaskCreateRequest,
        db: Session,
    ) -> Task:
        task = Task(
            project_id=project_id,
            name=data.name,
            description=data.description,
            is_alive=True,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_task(task_id: int, db: Session) -> Task | None:
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def update_task(task: Task, updates: dict, db: Session) -> Task:
        for field, value in updates.items():
            if hasattr(task, field) and value is not None:
                setattr(task, field, value)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def soft_delete_task(task: Task, db: Session) -> Task:
        task.is_alive = False
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_tasks(
        project_id: int,
        is_alive_filters: list[bool],
        current_user: dict,
        db: Session,
    ) -> list[Task]:
        query = (
            db.query(Task)
            .filter(Task.project_id == project_id)
            .filter(Task.is_alive.in_(is_alive_filters))
        )
        
        if "admin" not in current_user.get("user_roles", []):
            query = (
                query.join(
                    ProjectAssignment,
                    Task.project_id == ProjectAssignment.project_id,
                )
                .filter(ProjectAssignment.user_id == current_user["user_id"])
                .filter(ProjectAssignment.is_assigned.is_(True))
            )
        return query.order_by(Task.name.asc()).all()

