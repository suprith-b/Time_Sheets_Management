from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict
from app.models.ProjectModel import StatusEnum



class CreateProject(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    status: Optional[StatusEnum] = StatusEnum.CREATED

class EditProject(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[StatusEnum] = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    manager_id: Optional[int] = None
    description: Optional[str] = None
    start_date: date
    end_date: date
    status: StatusEnum