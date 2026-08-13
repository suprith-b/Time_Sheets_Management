from datetime import date, datetime, time
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.models.TimeLogModel import TimeLog, TypeEnum
from app.models.ProjectModel import Project
from app.models.TaskModel import Task
from app.repositories.ProjectRepository import ProjectRepository
import app.schemas.TimeLogSchema as TimeLogSchema



class TimeLogRepository:

    @staticmethod
    def get_total_hours(
        user_id: int,
        start_date: date | None,
        end_date: date | None,
        type_filters: list[TypeEnum] | None,
        db: Session,
    ) -> float:
        query = db.query(TimeLog).filter(TimeLog.user_id == user_id)

        if start_date is not None:
            query = query.filter(TimeLog.start_time >= datetime.combine(start_date, time.min))

        if end_date is not None:
            query = query.filter(TimeLog.start_time <= datetime.combine(end_date, time.max))

        if type_filters:
            query = query.filter(TimeLog.type.in_(type_filters))

        total_minutes = sum(
            (log.end_time - log.start_time).total_seconds() / 60.0 for log in query.all() if log.end_time
        )
        return round(total_minutes / 60.0, 2)  # Convert minutes to hours and round to 2 decimal places

    @staticmethod
    def is_valid_project_and_task(project_id: int, task_id: int, user_id: int, db: Session) -> bool:
        if not ProjectRepository.are_projects_assigned([project_id], user_id, db):
            return False
        task_exists = db.query(Task.id).filter(Task.id == task_id, Task.project_id == project_id).first() is not None
        return task_exists

    @staticmethod
    def create_time_logs(user_id: int, time_logs: list[TimeLogSchema.TimeLogCreateItem], db: Session):
        if not time_logs:
            return
        log_dicts = [
            {
                "user_id": user_id,
                "project_id": item.project_id,
                "task_id": item.task_id,
                "start_time": item.start_time,
                "end_time": item.end_time,
                "type": item.type,
                "comments": item.comments,
            }
            for item in time_logs
        ]
        if log_dicts:
            db.execute(insert(TimeLog).values(log_dicts))
        db.commit()

    @staticmethod
    def get_user_timelogs(
        user_id: int,
        project_ids: list[int] | None,
        start_date: datetime | None,
        end_date: datetime | None,
        type_filters: list[TypeEnum] | None,
        page: int | None,
        page_size: int | None,
        sort_by: str,
        sort_type: int,
        db: Session,
    ):
        query = (
            db.query(
                TimeLog.id,
                TimeLog.project_id,
                Project.name.label("project_name"),
                TimeLog.task_id,
                Task.name.label("task_name"),
                TimeLog.start_time,
                TimeLog.end_time,
                TimeLog.type,
                TimeLog.comments,
            )
            .join(Project, TimeLog.project_id == Project.id)
            .join(Task, TimeLog.task_id == Task.id)
            .filter(TimeLog.user_id == user_id)
        )

        if project_ids:
            query = query.filter(TimeLog.project_id.in_(project_ids))

        if start_date is not None:
            query = query.filter(TimeLog.start_time >= start_date)

        if end_date is not None:
            query = query.filter(TimeLog.start_time <= end_date)


        if type_filters:
            query = query.filter(TimeLog.type.in_(type_filters))

        if sort_by == "project_name":
            sort_column = Project.name
        elif sort_by == "start_time":
            sort_column = TimeLog.start_time

        if sort_type == -1:
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()

        query = query.order_by(sort_column)
        if page is not None and page_size is not None:
            offset = (page - 1) * page_size
            query = query.offset(offset).limit(page_size)
        return query.all()


    @staticmethod
    def get_timelog_by_id(timelog_id: int, db: Session) -> TimeLog | None:
        return db.query(TimeLog).filter(TimeLog.id == timelog_id).first()

    @staticmethod
    def update_timelog(timelog: TimeLog, updates: dict, db: Session) -> TimeLog:
        for field, value in updates.items():
            if hasattr(timelog, field) and value is not None:
                setattr(timelog, field, value)
        db.commit()
        db.refresh(timelog)
        return timelog
