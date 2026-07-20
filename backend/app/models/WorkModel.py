from sqlalchemy import Column, Integer, String, Foreignkey, TIMESTAMP, Enum as SQLEnum
from app.db.database import Base
from enum import Enum

class TypeEnum( Base ):
    STANDARD = "standard"
    OVERTIME = "over_time"

class Work( Base ):
    __tablename__ = "works"

    id = Column( Integer, primary_key = True, autoincrement = True )
    user_id = Column( Integer, Foreignkey( "users.id" ) )
    task_id = Column( Integer, Foreignkey( "tasks.id" ) )
    start_time = Column( TIMESTAMP )
    end_time = Column( TIMESTAMP )
    comments = Column( String( 500 ) )
    type = Column( SQLEnum( TypeEnum ), nullable = False )
