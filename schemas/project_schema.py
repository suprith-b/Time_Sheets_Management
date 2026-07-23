from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProjectStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"


class ProjectCreate(BaseModel):
    name: str = Field(max_length=50)
    description: Optional[str] = Field(default=None, max_length=300)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: ProjectStatus = ProjectStatus.created


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=50)
    description: Optional[str] = Field(default=None, max_length=300)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[ProjectStatus] = None


class ProjectRead(ProjectCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
