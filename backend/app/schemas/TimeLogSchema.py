from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.TimeLogModel import TypeEnum


class TimeLogCreateItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: int
    task_id: int
    start_time: datetime
    end_time: datetime
    type: TypeEnum
    comments: str | None = None


class CreateTimeLogsRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    time_logs: list[TimeLogCreateItem]


class TimeLogUpdateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: int | None = None
    task_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    type: TypeEnum | None = None
    comments: str | None = None


class TimeLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    project_id: int
    task_id: int
    start_time: datetime
    end_time: datetime
    type: TypeEnum
    comments: str | None = None


class TimeLogDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    project_name: str
    task_id: int
    task_name: str
    start_time: datetime
    end_time: datetime
    type: TypeEnum


class TimeLogMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message: str

class TimeLogHoursResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_hours: float