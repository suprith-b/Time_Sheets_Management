from pydantic import BaseModel, ConfigDict


class ManagerAssignmentCreate(BaseModel):
    employee_id: int
    manager_id: int


class ManagerAssignmentRead(ManagerAssignmentCreate):
    model_config = ConfigDict(from_attributes=True)
