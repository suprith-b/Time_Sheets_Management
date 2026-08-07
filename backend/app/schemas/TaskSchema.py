from pydantic import BaseModel, ConfigDict
from typing import Optional

class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    description: Optional[str] = None
    is_alive: Optional[bool] = None

class TaskCreateRequest(TaskBase):
    name: str
    description: Optional[ str ] = None

class TaskUpdateRequest(TaskBase):
    pass

class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    name: str
    description: Optional[str] = None
    is_alive: bool
