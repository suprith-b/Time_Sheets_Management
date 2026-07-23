from sqlalchemy import Column, ForeignKey, Integer
from app.db.database import Base

class ProjectAssignment( Base ):
    __tablename__ = "project_assignments"

    user_id = Column( Integer, ForeignKey( "users.id" ), primary_key = True )
    project_id = Column( Integer, ForeignKey( "projects.id" ), primary_key = True )
    
