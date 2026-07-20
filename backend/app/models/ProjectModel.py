from sqlalchemy import Column, Integer, String, Date, Enum as SQLEnum
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
    description = Column( String( 500 ) )
    start_date = Column( Date ) #yyyy-mm-dd
    end_date = Column( Date ) #yyyy-mm-dd
    status = Column( SQLEnum( StatusEnum ), nullable = False )
