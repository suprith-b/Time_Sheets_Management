from pydantic import BaseModel, ConfigDict

from app.models.RoleModel import RoleEnum as RE


class RoleAssignmentRequest(BaseModel):
    roles: list[RE]


class UsersRoleAssignmentRequest(BaseModel):
    users: list[int]
    roles: list[RE]


class UserListRequest(BaseModel):
    users: list[int]

class ProjectUserAssignmentRequest(BaseModel):
    users: list[int]
