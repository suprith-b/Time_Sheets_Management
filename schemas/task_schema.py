from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    project_id: int
    name: str = Field(max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)


class TaskRead(TaskCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
