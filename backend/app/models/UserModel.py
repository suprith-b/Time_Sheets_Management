from sqlalchemy import Column, Integer, String, Foreignkey
from app.db.database import Base

class User( Base ):
    __tablename__ = "users"

    id = Column( Integer, primary_key = True, autoincrement = True )
    username = Column( String( 30 ) )
    role_id = Column( Integer, Foreignkey( "roles.id" ) )
    name = Column( String( 50 ) )
    email = Column( String( 50 ) )
    password = Column( String( 60 ) )