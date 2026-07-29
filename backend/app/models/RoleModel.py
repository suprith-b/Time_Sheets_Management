from enum import Enum

from sqlalchemy import Column, Enum as SQLEnum, Integer

from app.db.database import Base


class RoleEnum(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(
        SQLEnum(RoleEnum, values_callable=lambda enum_class: [member.value for member in enum_class]),
        nullable=False,
    )
