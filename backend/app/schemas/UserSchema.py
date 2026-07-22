from pydantic import BaseModel, ConfigDict
from typing import Optional


class CreateUser(BaseModel):
    username: str
    role_id: int
    manager_id: Optional [ int ]
    name: str
    email: str
    password: str
    model_config = ConfigDict(from_attributes=True)

class EditUser(BaseModel):
    username: Optional[str]
    role_id: Optional[int]
    manager_id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    username: str
    role_id: int
    manager_id: Optional[int]
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)