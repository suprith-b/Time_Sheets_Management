from pydantic import BaseModel, ConfigDict
from typing import Optional

class AssignProjectsRequest(BaseModel):
    project_ids: list[int]


class AssignProjectsResponse(BaseModel):
    user_id: int
    project_ids: list[int]