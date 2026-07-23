from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class WorkType(str, Enum):
    standard = "standard"
    over_time = "over_time"


class WorkCreate(BaseModel):
    user_id: int
    task_id: int
    start_time: datetime
    end_time: datetime
    comments: Optional[str] = Field(default=None, max_length=500)
    type: WorkType = WorkType.standard


class WorkUpdate(BaseModel):
    task_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    comments: Optional[str] = Field(default=None, max_length=500)
    type: Optional[WorkType] = None


class WorkRead(WorkCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
