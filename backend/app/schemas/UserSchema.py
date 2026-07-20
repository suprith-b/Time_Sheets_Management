from pydantic import BaseModel

class CreateUser( BaseModel ):
    username: str
    role_id: int
    name: str
    email: str
    password: str