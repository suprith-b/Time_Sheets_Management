from pydantic import BaseModel, ConfigDict
from app.models.RoleModel import RoleEnum
from app.schemas.ProjectSchema import ProjectResponse

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str | None = None
    userid: str | None = None
    phone_number: str | None = None
    company_mail: str | None = None
    manager_id: int | None = None
    manager_userid: str | None = None
    manager_name: str | None = None
    roles: list[str] | None = None
    is_alive: int


class CreateUserRequest(BaseModel):
    userid: str
    username: str
    name: str
    phone_number: str
    company_mail: str
    password: str
    roles: list[RoleEnum] | None = None
    manager_id: int | None = None


class CreateUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    userid: str
    phone_number: str
    company_mail: str
    password: str
    roles: list[RoleEnum]
    manager_id: int | None = None
    manager_name: str | None = None


class EditUserRequest(BaseModel):
    name: str | None = None
    userid: str | None = None
    username: str | None = None
    phone_number: str | None = None
    company_mail: str | None = None
    roles: list[RoleEnum] | None = None
    manager_id: int | None = None
    is_alive: int | None = None


class UpdatePasswordRequest(BaseModel):
    password: str
