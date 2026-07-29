from app.utils.security import hash_password
from app.utils.security import create_access_token
from jose import JWTError
from app.core.config import settings
from jose import jwt
from app.repositories.UserRepository import UserRepository
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.AuthRepository import AuthRepository
import app.schemas.AuthSchema as AuthSchema
from app.utils.security import verify_password


class AuthService:

    @staticmethod
    def login(data: AuthSchema.LoginRequest, db: Session):
        result = AuthRepository.get_user_with_password(data, db)
        if not result or not verify_password(data.password, result[ "pwd_entry" ].password ):
            if result:
                print( "original: ", hash_password( data.password ), "hashed:", result[ "pwd_entry" ].password)
            else:
                print( "no reuslt" )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
        
        user_id = payload.get("user_id")

        if user_id is None:
            print( "Invalid token payload" )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_details = UserRepository.get_user_by_id( user_id, db )
        
        if user_details is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user, roles = user_details[ "user" ], user_details[ "roles" ]
        return AuthSchema.LoginResponse(
            id=user.id,
            userid=str( user.userid ),
            username="",
            name=user.name,
            roles=roles,
        )
