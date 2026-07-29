from sqlalchemy import Column, ForeignKey, Integer, text, Boolean

from app.db.database import Base

from app.models.RoleModel import Role
from app.models.UserModel import User

class RoleAssignment(Base):
    __tablename__ = "role_assignments"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    is_assigned = Column( Boolean, default=True, server_default=text("1"), nullable=False)