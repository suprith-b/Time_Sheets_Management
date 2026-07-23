from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_

import app.schemas.WorkSchema as WorkSchema
from app.models.TaskModel import Task
from app.models.RoleModel import Role, RoleEnum
from app.models.UserModel import User
from app.models.WorkModel import TypeEnum, Work
from typing import Optional


class WorkRepository:
    @staticmethod
    def _filtered_work_query(
        project_ids: Optional[list[int]],
        types: list[TypeEnum],
        start_time: datetime,
        end_time: datetime,
        db: Session,
    ):
        query = db.query(Work).join(Task, Task.id == Work.task_id).filter(
            Work.start_time >= start_time,
            Work.end_time <= end_time,
            Work.type.in_(types),
        )
        if project_ids:
            query = query.filter(Task.project_id.in_(project_ids))
        return query

    @staticmethod
    def create_works(
        user_id: int,
        works_data: list[WorkSchema.CreateWork],
        db: Session,
    ):
        works = [
            Work(user_id=user_id, **work_data.model_dump())
            for work_data in works_data
        ]
        db.add_all(works)
        db.commit()
        for work in works:
            db.refresh(work)
        return works

    @staticmethod
    def get_work_by_id(work_id: int, db: Session):
        return db.query(Work).filter(Work.id == work_id).first()

    @staticmethod
    def edit_work(
        work_id: int,
        data: WorkSchema.EditWork,
        db: Session,
    ):
        work = WorkRepository.get_work_by_id(work_id, db)
        if work is None:
            return None

        for key in data.model_fields_set:
            setattr(work, key, getattr(data, key))

        db.commit()
        db.refresh(work)
        return work

    @staticmethod
    def delete_work(work_id: int, db: Session):
        work = WorkRepository.get_work_by_id(work_id, db)
        if work is None:
            return None

        db.delete(work)
        db.commit()
        return work

    @staticmethod
    def get_works(
        user_id: int,
        project_ids: Optional[list[int]],
        types: list[TypeEnum],
        start_time: datetime,
        end_time: datetime,
        db: Session,
    ):
        return WorkRepository._filtered_work_query(
            project_ids,
            types,
            start_time,
            end_time,
            db,
        ).filter(Work.user_id == user_id).all()

    @staticmethod
    def get_report_works(
        roles: list[RoleEnum],
        current_user: dict,
        project_ids: Optional[list[int]],
        types: list[TypeEnum],
        start_time: datetime,
        end_time: datetime,
        db: Session,
    ):
        query = WorkRepository._filtered_work_query(
            project_ids,
            types,
            start_time,
            end_time,
            db,
        ).join(User, User.id == Work.user_id).join(Role, Role.id == User.role_id)

        if current_user["user_role"] == "manager":
            query = query.filter(
                User.manager_id == current_user["user_id"],
                Role.role == RoleEnum.EMPLOYEE,
            )
        else:
            query = query.filter(Role.role.in_(roles))

        return query.with_entities(
            Work.user_id,
            Task.project_id,
            Work.start_time,
            Work.end_time,
        ).all()
