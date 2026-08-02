from datetime import datetime
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.models.RoleModel import RoleEnum as RE
from app.models.TimeLogModel import TimeLog, TypeEnum
from app.models.UserModel import User
from app.models.ProjectModel import Project


class AnalyticsRepository:

    @staticmethod
    def get_report_data(
        as_role: str,
        start_date: datetime,
        end_date: datetime,
        project_ids: list[int] | None,
        type_filters: list[TypeEnum],
        sort_by: str,
        sort_type: int,
        current_user_id: int,
        db: Session,
    ):
        total_minutes = func.sum(
            func.timestampdiff(text("MINUTE"), TimeLog.start_time, TimeLog.end_time)
        ).label("total_minutes")

        query = (
            db.query(
                User.id.label("id"),
                User.name.label("name"),
                User.userid.label("userid"),
                Project.id.label("project_id"),
                Project.name.label("project_name"),
                total_minutes,
            )
            .join(User, TimeLog.user_id == User.id)
            .join(Project, TimeLog.project_id == Project.id)
            .filter(TimeLog.start_time >= start_date)
            .filter(TimeLog.start_time <= end_date)
        )

        if as_role != RE.ADMIN:
            query = query.filter(User.manager_id == current_user_id)

        if project_ids:
            query = query.filter(TimeLog.project_id.in_(project_ids))

        if type_filters:
            query = query.filter(TimeLog.type.in_(type_filters))

        query = query.group_by(User.id, Project.id)

        if sort_by == "project_name":
            sort_column = Project.name
        elif sort_by == "name":
            sort_column = User.name
        else:
            sort_column = total_minutes

        if sort_type == -1:
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()

        query = query.order_by(sort_column)

        return query.all()
