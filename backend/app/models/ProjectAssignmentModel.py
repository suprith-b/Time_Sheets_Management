from sqlalchemy import Boolean
from sqlalchemy import Column, ForeignKey, Integer

from app.db.database import Base

from app.models.ProjectModel import Project
from app.models.UserModel import User

class ProjectAssignment(Base):
    __tablename__ = "project_assignments"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    is_assigned = Column( Boolean, default = True, server_default = "1", nullable = False )
