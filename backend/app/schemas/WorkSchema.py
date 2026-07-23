from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.WorkModel import TypeEnum
from app.models.RoleModel import RoleEnum


class CreateWork(BaseModel):
    task_id: int
    start_time: datetime
    end_time: datetime
    comments: Optional[str] = None
    type: TypeEnum


class EditWork(BaseModel):
    task_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    comments: Optional[str] = None
    type: Optional[TypeEnum] = None


class WorkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    start_time: datetime
    end_time: datetime
    comments: Optional[str] = None
    type: TypeEnum
    duration: int = 0


class WorkReportResponse(BaseModel):
    user_id: int
    project_id: int
    duration: int
