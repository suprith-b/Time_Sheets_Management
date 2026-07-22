from sqlalchemy.orm import Session
import app.schemas.UserSchema as UserSchema
from app.repositories.UserRepository import UserRepository


class UserService:

    @staticmethod
    def get_users(current_user: dict, db: Session):
        users = UserRepository.get_all_users(current_user, db)
        return [UserSchema.UserResponse.model_validate(user) for user in users]

    @staticmethod
    def get_user(current_user: dict, user_id: int, db: Session):
        user = UserRepository.get_user_by_id(user_id, db)
        if user is None:
            return None
        return UserSchema.UserResponse.model_validate(user)

    @staticmethod
    def create_user(data: UserSchema.CreateUser, db: Session):
        user = UserRepository.create_user(data, db)
        return UserSchema.UserResponse.model_validate(user)

    @staticmethod
    def delete_user(user_id: int, db: Session):
        user = UserRepository.delete_user(user_id, db)
        if user is None:
            return None
        return UserSchema.UserResponse.model_validate(user)

    @staticmethod
    def edit_user(user_id: int, data: UserSchema.EditUser, db: Session):
        user = UserRepository.edit_user(user_id, data, db)
        if user is None:
            return None
        return UserSchema.UserResponse.model_validate(user)