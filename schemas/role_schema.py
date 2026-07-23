from enum import Enum

from pydantic import BaseModel, ConfigDict


class RoleName(str, Enum):
    employee = "employee"
    manager = "manager"
    admin = "admin"


class RoleCreate(BaseModel):
    role: RoleName


class RoleRead(RoleCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
