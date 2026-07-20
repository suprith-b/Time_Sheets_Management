from sqlalchemy.orm import Session
from app.models.UserModel import User
import app.schemas.UserSchema as UserSchema


class UserRepository:

    @staticmethod
    def create_user(
        data: UserSchema.CreateUser,
        db: Session
    ):
        user = User(
            username=data.username,
            role_id=data.role_id,
            name=data.name,
            email=data.email,
            password=data.password,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        return user