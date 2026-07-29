from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text

from app.db.database import Base

from app.models.ProjectModel import Project


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String(100))
    description = Column(String(300))
    is_alive = Column("isAlive", Boolean, default=True, server_default=text("1"), nullable=False)
