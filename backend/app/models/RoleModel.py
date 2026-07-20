from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from app.db.database import Base
from enum import Enum

class RoleEnum ( Enum ):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"

class Role ( Base ):
    __tablename__ = "roles"

    id = Column( Integer, primary_key = True, autoincrement = True )
    role = Column( SQLEnum( RoleEnum ), nullable = False )