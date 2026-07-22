from pydantic import BaseModel, ConfigDict
from typing import Optional


class CreateUserRequest(BaseModel):

    username: str
    role_id: int
    manager_id: Optional [ int ] = None
    name: str
    email: str
    password: str

class CreateUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role_id: int
    manager_id: Optional [ int ] = None
    name: str
    email: str
    password: str

class EditUser(BaseModel):
    username: Optional[str] = None
    role_id: Optional[int] = None
    manager_id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role_id: int
    manager_id: Optional[int] = None
    name: str
    email: str