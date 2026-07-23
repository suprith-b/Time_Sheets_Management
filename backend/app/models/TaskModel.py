from sqlalchemy import Column, ForeignKey, Integer, String
from app.db.database import Base
from app.models.ProjectModel import Project

class Task ( Base ):
    __tablename__ = "tasks"

    id = Column( Integer, primary_key = True, autoincrement = True )
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column( String( 50 ) )
    description = Column( String( 200 ) )