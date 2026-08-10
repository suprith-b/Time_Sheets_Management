from app.repositories.UserRepository import UserRepository
from app.utils.security import verify_password
from enum import verify
from app.schemas import AuthSchema
from sqlalchemy.orm import Session

from app.models.PasswordModel import Password
from app.models.RoleAssignmentModel import RoleAssignment
from app.models.RoleModel import Role
from app.models.UserModel import User


class AuthRepository:

    @staticmethod
    def get_user_with_password(data: AuthSchema.LoginRequest, db: Session):
        user = db.query( User ).filter( User.company_mail == data.company_mail ).first()
        if user is None:
            return None
        pwd_entry = db.query( Password ).filter( Password.user_id == user.id ).first()
        if pwd_entry is None:
            return None
        return { "user": user, "pwd_entry": pwd_entry}
    
    @staticmethod
    def validate_user_password( user_id: int, password: str, db: Session ) -> bool:
        pwd_entry = db.query( Password ).filter( Password.user_id == user_id ).first()
        if pwd_entry is None:
            return False
        return verify_password( password, pwd_entry.password )
        