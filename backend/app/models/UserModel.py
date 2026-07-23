from sqlalchemy import Column, ForeignKey, Integer, String
from app.db.database import Base

class User( Base ):
    __tablename__ = "users"

    id = Column( Integer, primary_key = True, autoincrement = True )
    username = Column( String( 30 ) )
    role_id = Column( Integer, ForeignKey( "roles.id" ) )
    name = Column( String( 50 ) )
    email = Column( String( 50 ) )
    password = Column( String( 60 ) )
    status = Column( String( 20 ), nullable = False, default = "active" )
