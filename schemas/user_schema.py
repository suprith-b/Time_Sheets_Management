from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(max_length=30)
    role_id: int
    name: str = Field(max_length=50)
    email: EmailStr
    password: str = Field(min_length=1, max_length=60)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, max_length=30)
    role_id: Optional[int] = None
    name: Optional[str] = Field(default=None, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=1, max_length=60)


class UserRead(BaseModel):
    id: int
    username: str
    role_id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
