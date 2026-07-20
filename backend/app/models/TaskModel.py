from sqlalchemy import Column, Integer, String, Foreignkey
from app.db.database import Base

class Task ( Base ):
    __tablename__ = "tasks"

    id = Column( Integer, primary_key = True, autoincrement = True )
    project_id = Column( Integer, Foreignkey( "projects.id" ) )
    name = Column( String( 50 ) )
    description = Column( String( 200 ) )