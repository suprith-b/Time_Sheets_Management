from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    company_mail: str
    password: str


class LoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    userid: str
    username: str
    name: str
    roles: list[str]