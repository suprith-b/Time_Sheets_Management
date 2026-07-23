from datetime import date, time
from typing import Optional

from pydantic import BaseModel, Field, model_validator

from app.models.WorkModel import TypeEnum


class TimesheetEntryRequest(BaseModel):
    task_id: int
    work_date: date
    start_time: time
    end_time: time
    type: TypeEnum = TypeEnum.STANDARD
    comments: Optional[str] = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def times_are_valid(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class TimesheetSubmitRequest(BaseModel):
    user_id: int
    entries: list[TimesheetEntryRequest] = Field(min_length=1)
