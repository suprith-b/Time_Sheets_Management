from sqlalchemy import Column, Integer, String, Foreignkey
from app.db.database import Base
from app.models.UserModel import User
from app.models.ProjectModel import Project


class ProjectAssignment( Base ):
    __tablename__ = "project_assignments"

    user_id = Column( Integer, Foreignkey( "users.id" ), primary_key = True )
    project_id = Column( Integer, Foreignkey( "projects.id" ), primary_key = True )
    