from sqlalchemy.orm import Session

import app.schemas.TaskSchema as TaskSchema
from app.models.TaskModel import Task


class TaskRepository:
    @staticmethod
    def get_tasks_by_project(project_id: int, db: Session):
        return db.query(Task).filter(Task.project_id == project_id).all()

    @staticmethod
    def get_task_by_id(task_id: int, db: Session):
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def create_task(project_id: int, data: TaskSchema.CreateTask, db: Session):
        task = Task(project_id=project_id, **data.model_dump())
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def edit_task(
        task_id: int,
        data: TaskSchema.EditTask,
        db: Session,
    ):
        task = TaskRepository.get_task_by_id(task_id, db)
        if task is None:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(task, key, value)

        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete_task(task_id: int, db: Session):
        task = TaskRepository.get_task_by_id(task_id, db)
        db.delete(task)
        db.commit()
        return task
