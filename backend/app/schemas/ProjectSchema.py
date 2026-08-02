from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional
from app.models.ProjectModel import StatusEnum
from app.schemas.TaskSchema import TaskCreateRequest

class ProjectBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: Optional[str] = None
    status: Optional[StatusEnum] = None
    duration: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProjectCreateRequest(ProjectBase):
    name: str
    status: Optional[StatusEnum] = StatusEnum.CREATED
    duration: int
    tasks: Optional[list[TaskCreateRequest]] | None = []

class ProjectUpdateRequest(ProjectBase):
    name: str | None = None
    description: str | None = None
    status: StatusEnum | None = None
    duration: int | None = None
    start_date: date | None = None
    end_date: date | None = None

class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: StatusEnum
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    duration: Optional[int] = None
    can_revoke_project: Optional[bool] = None
    num_tasks: Optional[int] | None = None