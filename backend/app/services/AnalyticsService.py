from datetime import datetime
from sqlalchemy.orm import Session

from app.models.RoleModel import RoleEnum as RE
from app.models.TimeLogModel import TypeEnum
from app.repositories.AnalyticsRepository import AnalyticsRepository
import app.schemas.AnalyticsSchema as AnalyticsSchema
from app.core.exceptions import AdminAccessRequiredError, ManagerAccessRequiredError


class AnalyticsService:

    @staticmethod
    def get_reports(
        as_role: str,
        start_date: datetime,
        end_date: datetime,
        project_ids: list[int] | None,
        type_filters: list[TypeEnum],
        sort_by: str,
        sort_type: int,
        current_user: dict,
        db: Session,
    ) -> list[AnalyticsSchema.ReportResponse]:
        user_roles = current_user.get("user_roles", [])

        if as_role == RE.ADMIN and RE.ADMIN not in user_roles:
            raise AdminAccessRequiredError()
        if as_role == RE.MANAGER and RE.MANAGER not in user_roles:
            raise ManagerAccessRequiredError()

        rows = AnalyticsRepository.get_report_data(
            as_role=as_role,
            start_date=start_date,
            end_date=end_date,
            project_ids=project_ids,
            type_filters=type_filters,
            sort_by=sort_by,
            sort_type=sort_type,
            current_user_id=current_user["user_id"],
            db=db,
        )

        return [
            AnalyticsSchema.ReportResponse(
                id=row.id,
                name=row.name or "",
                userid=row.userid or "",
                project_id=row.project_id,
                project_name=row.project_name or "",
                hours=round(float(row.total_minutes or 0) / 60.0, 2),
            )
            for row in rows
        ]
