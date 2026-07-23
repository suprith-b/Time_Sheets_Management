from pydantic import BaseModel, ConfigDict


class ProjectAssignmentCreate(BaseModel):
    user_id: int
    project_id: int


class ProjectAssignmentRead(ProjectAssignmentCreate):
    model_config = ConfigDict(from_attributes=True)
