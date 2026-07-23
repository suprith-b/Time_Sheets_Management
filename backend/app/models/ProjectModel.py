from sqlalchemy import Column, Integer, String, Date, Enum as SQLEnum, Text
from app.db.database import Base
from enum import Enum

class StatusEnum ( Enum ):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Project( Base ):
    __tablename__ = "projects"

    id = Column( Integer, primary_key = True, autoincrement = True )
    name = Column( String( 50 ) )
    description = Column( String( 300 ) )
    start_date = Column( Date ) #yyyy-mm-dd
    end_date = Column( Date ) #yyyy-mm-dd
    status = Column( SQLEnum( StatusEnum, values_callable = lambda values: [ value.value for value in values ] ), nullable = False )
    active_status = Column( String( 20 ), nullable = False, default = "active" )
    project_image = Column( Text )
