from enum import Enum

from sqlalchemy import Column, Enum as SQLEnum, Integer, String, TIMESTAMP, ForeignKey

from app.db.database import Base

from app.models.TaskModel import Task
from app.models.ProjectAssignmentModel import ProjectAssignment

class TypeEnum(str, Enum):
    STANDARD = "standard"
    OVERTIME = "overtime"


class TimeLog(Base):
    __tablename__ = "time_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("project_assignments.user_id"), nullable=False)
    project_id = Column(Integer, ForeignKey( "project_assignments.project_id"), nullable=False)
    manager_id = Column( Integer, ForeignKey( "users.id" ), nullable = True )
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False )
    start_time = Column(TIMESTAMP(timezone=True))
    end_time = Column(TIMESTAMP(timezone=True))
    type = Column(
        SQLEnum(TypeEnum, values_callable=lambda enum_class: [member.value for member in enum_class]),
        nullable=False,
    )
    comments = Column(String(300))
