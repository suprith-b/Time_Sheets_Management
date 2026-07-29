from sqlalchemy import ForeignKey
from enum import unique
from sqlalchemy import Boolean, Column, Integer, String, text

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    manager_id = Column( Integer, ForeignKey( "users.id" ), nullable = True )
    userid = Column( String( 10 ), unique=True )
    name = Column(String(80))
    company_mail = Column(String(50), unique=True)
    personal_mail = Column(String(50), unique=True)
    is_alive = Column("isAlive", Boolean, default=True, server_default=text("1"), nullable=False)
