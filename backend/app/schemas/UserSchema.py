from pydantic import BaseModel, ConfigDict
from app.models.RoleModel import RoleEnum
from app.schemas.ProjectSchema import ProjectResponse


class UserDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    userid: str
    username: str
    name: str
    personal_mail: str | None = None
    company_mail: str | None = None
    is_alive: bool
    roles: list[str]
    projects: list[ProjectResponse]
    manager_id: int | None = None
    manager_name: str | None = None



class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    userid: str
    manager_id: int | None = None
    manager_name: str | None = None
    roles: list[str] | None = None
    is_alive: int


class CreateUserRequest(BaseModel):
    userid: str
    username: str
    name: str
    personal_mail: str
    company_mail: str
    password: str
    roles: list[RoleEnum] | None = None


class CreateUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    userid: str
    personal_mail: str
    company_mail: str
    password: str
    roles: list[str]


class EditUserRequest(BaseModel):
    name: str | None = None
    userid: str | None = None
    username: str | None = None
    personal_mail: str | None = None
    company_mail: str | None = None
    is_alive: int | None = None


class UpdatePasswordRequest(BaseModel):
    password: str
