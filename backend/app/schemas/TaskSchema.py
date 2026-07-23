from typing import Optional

from pydantic import BaseModel, ConfigDict


class CreateTask(BaseModel):
    name: str
    description: Optional[str] = None


class EditTask(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    name: str
    description: Optional[str] = None
