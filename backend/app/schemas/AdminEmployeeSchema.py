from typing import Optional
from typing import Literal

from pydantic import BaseModel, Field

from app.models.RoleModel import RoleEnum


class EmployeeCreateRequest(BaseModel):
    username: str = Field(min_length=1, max_length=30)
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    role: RoleEnum
    status: Literal["active", "inactive"] = "active"
    manager_id: Optional[int] = None
    project_ids: list[int] = []


class EmployeeUpdateRequest(BaseModel):
    username: Optional[str] = Field(default=None, min_length=1, max_length=30)
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    email: Optional[str] = Field(default=None, min_length=3, max_length=50)
    role: Optional[RoleEnum] = None
    status: Optional[Literal["active", "inactive"]] = None


class ManagerAssignmentRequest(BaseModel):
    manager_id: Optional[int] = None


class ProjectAssignmentRequest(BaseModel):
    project_ids: list[int]
