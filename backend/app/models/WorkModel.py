from sqlalchemy import Column, Enum as SQLEnum, ForeignKey, Integer, String, TIMESTAMP
from app.db.database import Base
from enum import Enum

class TypeEnum( Enum ):
    STANDARD = "standard"
    OVERTIME = "over_time"

class Work( Base ):
    __tablename__ = "works"

    id = Column( Integer, primary_key = True, autoincrement = True )
    user_id = Column( Integer, ForeignKey( "users.id" ) )
    task_id = Column( Integer, ForeignKey( "tasks.id" ) )
    start_time = Column( TIMESTAMP )
    end_time = Column( TIMESTAMP )
    comments = Column( String( 500 ) )
    type = Column( SQLEnum( TypeEnum, values_callable = lambda values: [ value.value for value in values ] ), nullable = False )
