from sqlalchemy import Column, ForeignKey, Integer
from app.db.database import Base

class ManagerAssignment( Base ):
    __tablename__ = "manager_assignments"

    employee_id = Column( Integer, ForeignKey( "users.id" ), primary_key = True )
    manager_id = Column( Integer, ForeignKey( "users.id" ), primary_key = True )
    
