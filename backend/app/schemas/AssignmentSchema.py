from pydantic import BaseModel, ConfigDict
from app.models.RoleModel import RoleEnum


class AssignUsersToManagerRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    employee_ids: list[int]


class ProjectAssignmentRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_ids: list[int]
    project_ids: list[int]


class RoleAssignmentRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_ids: list[int]
    roles: list[RoleEnum]


class AssignUsersToProjectRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_ids: list[int]


class AssignProjectsToUserRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_ids: list[int]


class AssignRolesToUserRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    roles: list[RoleEnum]


class AssignmentMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message: str
