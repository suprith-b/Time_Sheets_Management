from datetime import datetime
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.TimeLogModel import TypeEnum
import app.schemas.TimeLogSchema as TimeLogSchema
from app.services.TimeLogService import TimeLogService
from app.utils.RoleValidation import RoleValidation

router = APIRouter(prefix="/timelogs")


@router.post(
    "/{user_id}",
    response_model=TimeLogSchema.TimeLogMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_time_logs(
    user_id: int,
    data: TimeLogSchema.CreateTimeLogsRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin", "employee"])
    return TimeLogService.create_time_logs(user_id, data, current_user, db)


@router.get(
    "/{user_id}",
    response_model=list[TimeLogSchema.TimeLogDetailResponse],
)
def get_user_timelogs(
    user_id: int,
    project_ids: list[int] | None = Query(default=None),
    start_date: datetime | None = Query(default=datetime(1970, 1, 1)),
    end_date: datetime | None = Query(default_factory=datetime.now),
    type: list[TypeEnum] | None = Query(default=None),
    sort_by: str = Query(default="start_time"),
    sort_type: int = Query(default=-1),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin", "manager", "employee"])
    return TimeLogService.get_user_timelogs(
        user_id=user_id,
        project_ids=project_ids,
        start_date=start_date,
        end_date=end_date,
        type_filters=type,
        sort_by=sort_by,
        sort_type=sort_type,
        current_user=current_user,
        db=db,
    )

@router.get( "/hours/{user_id}", response_model=TimeLogSchema.TimeLogHoursResponse, )
def get_user_timelog_hours(
    user_id: int,
    start_date: datetime | None = Query(default=datetime(1970, 1, 1)),
    end_date: datetime | None = Query(default_factory=datetime.now),
    type: list[TypeEnum] | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin", "manager", "employee"])

    return TimeLogService.get_user_hours(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        type_filters=type,
        current_user=current_user,
        db=db,
    )



@router.patch(
    "/{timelog_id}",
    response_model=TimeLogSchema.TimeLogResponse,
)
def update_timelog(
    timelog_id: int,
    data: TimeLogSchema.TimeLogUpdateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, ["admin"])
    return TimeLogService.update_timelog(timelog_id, data, db)
