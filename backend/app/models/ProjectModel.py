from enum import Enum

from sqlalchemy import Column, Date, Enum as SQLEnum, Integer, String

from app.db.database import Base


class StatusEnum(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    duration = Column( Integer )
    status = Column(
        SQLEnum(StatusEnum, values_callable=lambda enum_class: [member.value for member in enum_class]),
        nullable=False,
    )
