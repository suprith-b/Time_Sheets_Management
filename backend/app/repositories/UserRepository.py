from sqlalchemy.orm import Session
from app.models.UserModel import User
import app.schemas.UserSchema as UserSchema
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher


password_hash = PasswordHash((BcryptHasher(),))


class UserRepository:

    @staticmethod
    def get_all_users(current_user: dict, db: Session):
        if ( current_user["user_role"] == "admin" ):
            return db.query(User).all()
        return db.query(User).filter( User.manager_id == current_user["user_id"] ).all()

    @staticmethod
    def get_user_by_id(user_id: int, db: Session):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(data: UserSchema.CreateUser, db: Session):
        user = User(
            username=data.username,
            role_id=data.role_id,
            manager_id=data.manager_id if data.role_id == 3 else None,
            name=data.name,
            email=data.email,
            password=password_hash.hash(data.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(user_id: int, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None
        db.delete(user)
        db.commit()
        return user

    @staticmethod
    def edit_user(user_id: int, data: UserSchema.EditUser, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            if value is None:
                continue
            if key == "role_id" and value != 3:
                setattr(user, "manager_id", None)
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user