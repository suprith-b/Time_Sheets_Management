from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.TimeLogModel import TypeEnum
from app.repositories.ProjectRepository import ProjectRepository
from app.repositories.TimeLogRepository import TimeLogRepository
from app.repositories.AssignmentRepository import AssignmentRepository
import app.schemas.TimeLogSchema as TimeLogSchema


class TimeLogService:

    @staticmethod
    def create_time_logs(
        user_id: int,
        data: TimeLogSchema.CreateTimeLogsRequest,
        current_user: dict,
        db: Session,
    ) -> TimeLogSchema.TimeLogMessageResponse:
        user_roles = current_user.get("user_roles", [])
        if "admin" not in user_roles:
            if current_user.get("user_id") != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to perform this action",
                )

        for item in data.time_logs:
            if item.start_time > item.end_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="start_time must be less than or equal to end_time",
                )
            if not TimeLogRepository.is_valid_project_and_task(item.project_id, item.task_id, user_id, db):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid project_id {item.project_id} or task_id {item.task_id}",
                )

        TimeLogRepository.create_time_logs(user_id, data.time_logs, db)
        return TimeLogSchema.TimeLogMessageResponse(message="Time logs successfully created")

    @staticmethod
    def get_user_timelogs(
        user_id: int,
        project_ids: list[int] | None,
        start_date: datetime | None,
        end_date: datetime | None,
        type_filters: list[TypeEnum] | None,
        sort_by: str,
        sort_type: int,
        current_user: dict,
        db: Session,
    ) -> list[TimeLogSchema.TimeLogDetailResponse]:
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
                    detail="You do not have permission to access this resource",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        rows = TimeLogRepository.get_user_timelogs(
            user_id=user_id,
            project_ids=project_ids,
            start_date=start_date,
            end_date=end_date,
            type_filters=type_filters,
            sort_by=sort_by,
            sort_type=sort_type,
            db=db,
        )
        return [TimeLogSchema.TimeLogDetailResponse.model_validate(r) for r in rows]


    @staticmethod
    def update_timelog(
        timelog_id: int,
        data: TimeLogSchema.TimeLogUpdateRequest,
        db: Session,
    ) -> TimeLogSchema.TimeLogResponse:
        timelog = TimeLogRepository.get_timelog_by_id(timelog_id, db)
        if not timelog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="TimeLog not found",
            )

        effective_project_id = data.project_id if data.project_id is not None else timelog.project_id
        effective_task_id = data.task_id if data.task_id is not None else timelog.task_id

        if data.project_id is not None or data.task_id is not None:
            if not TimeLogRepository.is_valid_project_and_task(effective_project_id, effective_task_id, timelog.user_id, db):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid project_id or task_id",
                )

        effective_start_time = data.start_time if data.start_time is not None else timelog.start_time
        effective_end_time = data.end_time if data.end_time is not None else timelog.end_time

        if data.start_time is not None or data.end_time is not None:
            if effective_start_time > effective_end_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="start_time must be less than or equal to end_time",
                )

        updates = data.model_dump(exclude_none=True)
        updated_log = TimeLogRepository.update_timelog(timelog, updates, db)
        return TimeLogSchema.TimeLogResponse.model_validate(updated_log)

