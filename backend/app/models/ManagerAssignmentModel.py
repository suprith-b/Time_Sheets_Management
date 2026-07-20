from sqlalchemy import Column, Integer, String, Foreignkey
from app.db.database import Base

class ManagerAssignment( Base ):
    __tablename__ = "manager_assignments"

    employee_id = Column( Integer, Foreignkey( "users.id" ), primary_key = True )
    manager_id = Column( Integer, Foreignkey( "users.id" ), primary_key = True )
    