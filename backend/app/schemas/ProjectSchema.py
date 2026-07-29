from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional
from app.models.ProjectModel import StatusEnum

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

class ProjectUpdateRequest(ProjectBase):
    pass

class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: StatusEnum
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    duration: Optional[int] = None