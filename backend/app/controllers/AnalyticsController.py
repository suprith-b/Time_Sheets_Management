from app.core.exceptions import ManagerAccessRequiredError
from app.core.exceptions import AdminAccessRequiredError
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
    view_as: list[ RE ] = Query( default = [ ] ),
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
    if len( view_as ) == 0:
        if RE.MANAGER in current_user[ "user_roles" ]:
            view_as.append( RE.MANAGER )
        if RE.ADMIN in current_user[ "user_roles" ]:
            view_as.append( RE.ADMIN )
    
    for role in view_as:
        if role == RE.ADMIN and RE.ADMIN not in current_user[ "user_roles" ]:
            raise AdminAccessRequiredError()
        if role == RE.MANAGER and RE.MANAGER not in current_user[ "user_roles" ]:
            raise ManagerAccessRequiredError()
            
    return AnalyticsService.get_reports(
        view_as=view_as,
        start_date=start_date,
        end_date=end_date,
        project_ids=project_ids,
        type_filters=type,
        sort_by=sort_by,
        sort_type=sort_type,
        current_user=current_user,
        db=db,
    )
