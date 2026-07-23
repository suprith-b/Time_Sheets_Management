from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import app.schemas.WorkSchema as WorkSchema
from app.models.WorkModel import TypeEnum, Work
from app.models.RoleModel import RoleEnum
from app.repositories.TaskRepository import TaskRepository
from app.repositories.UserRepository import UserRepository
from app.repositories.WorkRepository import WorkRepository


class WorkService:
    SORT_FIELDS = {
        "start_time",
        "duration",
    }

    @staticmethod
    def _validate_time_range(start_time: datetime, end_time: datetime):
        if end_time < start_time:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="end_time must be greater than or equal to start_time",
            )

    @staticmethod
    def _validate_works(
        works_data: list[WorkSchema.CreateWork],
        db: Session,
    ):
        for work_data in works_data:
            WorkService._validate_time_range(
                work_data.start_time,
                work_data.end_time,
            )
            if TaskRepository.get_task_by_id(work_data.task_id, db) is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Task {work_data.task_id} not found",
                )

    @staticmethod
    def _to_response(work: Work):
        duration = int((work.end_time - work.start_time).total_seconds())
        return WorkSchema.WorkResponse.model_validate(work).model_copy(
            update={"duration": duration}
        )

    @staticmethod
    def create_works(
        user_id: int,
        works_data: list[WorkSchema.CreateWork],
        db: Session,
    ):
        WorkService._validate_works(works_data, db)
        works = WorkRepository.create_works(user_id, works_data, db)
        return [WorkService._to_response(work) for work in works]

    @staticmethod
    def edit_work(
        work_id: int,
        data: WorkSchema.EditWork,
        db: Session,
    ):
        work = WorkRepository.get_work_by_id(work_id, db)
        if work is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Work record not found",
            )

        changed_fields = data.model_dump(exclude_unset=True)
        if data.task_id is not None:
            if TaskRepository.get_task_by_id(data.task_id, db) is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Task {data.task_id} not found",
                )
        if any(
            field != "comments" and value is None
            for field, value in changed_fields.items()
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="One or more required fields are cannot be set to None",
            )

        start_time = changed_fields.get("start_time", work.start_time)
        end_time = changed_fields.get("end_time", work.end_time)
        WorkService._validate_time_range(start_time, end_time)

        work = WorkRepository.edit_work(work_id, data, db)
        return WorkService._to_response(work)

    @staticmethod
    def delete_work(work_id: int, db: Session):
        work = WorkRepository.delete_work(work_id, db)
        if work is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Work not found",
            )
        return WorkService._to_response(work)

    @staticmethod
    def _check_get_access(user_id: int, current_user: dict, db: Session):
        if current_user["user_role"] == "admin" or user_id == current_user["user_id"]:
            return

        if current_user["user_role"] == "manager" and UserRepository.get_user_by_id(
            user_id,
            current_user,
            db,
        ) is not None:
            return

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view these work records",
        )

    @staticmethod
    def get_works(
        user_id: int,
        current_user: dict,
        project_ids: Optional[list[int]],
        sort_by: str,
        sort_type: int,
        types: list[TypeEnum],
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        db: Session,
    ):
        WorkService._check_get_access(user_id, current_user, db)
        if sort_type not in {-1, 1}:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="sort_type must be 1 or -1",
            )
        if sort_by not in WorkService.SORT_FIELDS:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"sort_by must be one of {sorted(WorkService.SORT_FIELDS)}",
            )

        effective_start = start_time or datetime(1970, 1, 1)
        effective_end = end_time or datetime.now(timezone.utc).replace(tzinfo=None)
        if effective_start.tzinfo is not None:
            effective_start = effective_start.astimezone(timezone.utc).replace(
                tzinfo=None
            )
        if effective_end.tzinfo is not None:
            effective_end = effective_end.astimezone(timezone.utc).replace(
                tzinfo=None
            )
        WorkService._validate_time_range(effective_start, effective_end)
        works = WorkRepository.get_works(
            user_id,
            project_ids,
            types,
            effective_start,
            effective_end,
            db,
        )

        def sort_value(work: Work):
            if sort_by == "duration":
                value = (work.end_time - work.start_time).total_seconds()
            else:
                value = getattr(work, sort_by)
                if isinstance(value, TypeEnum):
                    value = value.value
            return (value is not None, value)
        works.sort(key=sort_value, reverse=sort_type == -1)
        return [WorkService._to_response(work) for work in works]

    @staticmethod
    def get_reports(
        current_user: dict,
        roles: list[RoleEnum],
        project_ids: Optional[list[int]],
        sort_by: str,
        sort_type: int,
        types: list[TypeEnum],
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        db: Session,
    ):
        if sort_type not in {-1, 1}:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="sort_type must be 1 or -1",
            )
        if sort_by not in WorkService.SORT_FIELDS:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "sort_by must be one of "
                    f"{sorted(WorkService.SORT_FIELDS)}"
                ),
            )

        effective_start = start_time or datetime(1970, 1, 1)
        effective_end = end_time or datetime.now(timezone.utc).replace(tzinfo=None)
        if effective_start.tzinfo is not None:
            effective_start = effective_start.astimezone(timezone.utc).replace(
                tzinfo=None
            )
        if effective_end.tzinfo is not None:
            effective_end = effective_end.astimezone(timezone.utc).replace(
                tzinfo=None
            )
        WorkService._validate_time_range(effective_start, effective_end)

        report_rows = WorkRepository.get_report_works(
            roles,
            current_user,
            project_ids,
            types,
            effective_start,
            effective_end,
            db,
        )
        grouped: dict[tuple[int, int], int] = {}
        for user_id, project_id, work_start, work_end in report_rows:
            key = (user_id, project_id)
            grouped[key] = grouped.get(key, 0) + int(
                (work_end - work_start).total_seconds()
            )

        reports = [
            WorkSchema.WorkReportResponse(
                user_id=user_id,
                project_id=project_id,
                duration=duration,
            )
            for (user_id, project_id), duration in grouped.items()
        ]
        reports.sort(
            key=lambda report: getattr(report, sort_by),
            reverse=sort_type == -1,
        )
        return reports
