from datetime import date
from typing import Optional
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.models.ProjectModel import StatusEnum


class ProjectCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=300)
    start_date: date
    end_date: date
    status: StatusEnum = StatusEnum.CREATED
    active_status: Literal["active", "inactive"] = "active"
    project_image: Optional[str] = None
    manager_id: Optional[int] = None

    @model_validator(mode="after")
    def dates_are_valid(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=300)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[StatusEnum] = None
    active_status: Optional[Literal["active", "inactive"]] = None
    project_image: Optional[str] = None


class ProjectManagerRequest(BaseModel):
    manager_id: Optional[int] = None


class TaskCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)


class TaskUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)
