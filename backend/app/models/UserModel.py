from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base
from app.models.RoleModel import Role


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    manager_id = Column(Integer, ForeignKey("users.id"))
    username = Column(String(30) )
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(60))