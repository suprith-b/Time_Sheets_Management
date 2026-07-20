from sqlalchemy.orm import Session
import app.schemas.UserSchema as UserSchema
from app.repositories.UserRepository import UserRepository


class UserService:

    @staticmethod
    def create_user(
        data: UserSchema.CreateUser,
        db: Session
    ):
        return UserRepository.create_user(data, db)