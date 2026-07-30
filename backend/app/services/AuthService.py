from jose import JWTError
from app.core.config import settings
from jose import jwt
from app.repositories.UserRepository import UserRepository
from sqlalchemy.orm import Session

from app.repositories.AuthRepository import AuthRepository
import app.schemas.AuthSchema as AuthSchema
from app.utils.security import verify_password
from app.core.exceptions import InvalidAuthenticationTokenError, InvalidCredentialsError


class AuthService:

    @staticmethod
    def login(data: AuthSchema.LoginRequest, db: Session):
        result = AuthRepository.get_user_with_password(data, db)
        if not result or not verify_password(data.password, result[ "pwd_entry" ].password ):
            raise InvalidCredentialsError()
        user, pwd_entry = result[ "user" ], result[ "pwd_entry" ]

        roles = UserRepository.get_user_roles(user.id, db)

        return AuthSchema.LoginResponse(
            id=user.id,
            userid=str( user.userid ),
            username=pwd_entry.username,
            name=user.name,
            roles=roles,
        )

    @staticmethod
    def refresh( token: str, db: Session ):
        try:
            payload = jwt.decode( 
                token, 
                settings.JWT_SECRET, 
                algorithms=settings.JWT_ALGORITHM, 
                options={"verify_aud" : False})
        except JWTError as exc:
            raise InvalidAuthenticationTokenError() from exc
        
        user_id = payload.get("user_id")

        if user_id is None:
            raise InvalidAuthenticationTokenError("Invalid token payload")
        
        user_details = UserRepository.get_user_by_id( user_id, db )
        
        if user_details is None:
            raise InvalidAuthenticationTokenError("Invalid token")
        
        user, roles = user_details[ "user" ], user_details[ "roles" ]
        return AuthSchema.LoginResponse(
            id=user.id,
            userid=str( user.userid ),
            username="",
            name=user.name,
            roles=roles,
        )
