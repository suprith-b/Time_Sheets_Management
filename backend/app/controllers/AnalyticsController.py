from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.RoleModel import RoleEnum as RE
from app.models.TimeLogModel import TypeEnum
import app.schemas.AnalyticsSchema as AnalyticsSchema
from app.services.AnalyticsService import AnalyticsService
from app.utils.RoleValidation import RoleValidation

router = APIRouter(prefix="/analytics")


@router.get("/reports", response_model=list[AnalyticsSchema.ReportResponse])
def get_reports(
    as_role: str = Query(alias="as"),
    start_date: datetime = Query(default=datetime(1970, 1, 1)),
    end_date: datetime = Query(default_factory=datetime.now),
    project_ids: list[int] | None = Query(default=None),
    type: list[TypeEnum] = Query(
        default=[TypeEnum.STANDARD, TypeEnum.OVERTIME],
    ),
    sort_by: str = Query(default="duration"),
    sort_type: int = Query(default=-1),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    RoleValidation.validate_role(current_user, [RE.ADMIN, RE.MANAGER])
    return AnalyticsService.get_reports(
        as_role=as_role,
        start_date=start_date,
        end_date=end_date,
        project_ids=project_ids,
        type_filters=type,
        sort_by=sort_by,
        sort_type=sort_type,
        current_user=current_user,
        db=db,
    )
