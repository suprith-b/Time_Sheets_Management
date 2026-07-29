from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.TimeLogModel import TypeEnum
from app.repositories.AnalyticsRepository import AnalyticsRepository
import app.schemas.AnalyticsSchema as AnalyticsSchema


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

        if as_role == "admin" and "admin" not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have admin access",
            )
        if as_role == "manager" and "manager" not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have manager access",
            )

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
