from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from app.core.config import settings
from app.core.exceptions import AccessTokenMissingError, InvalidAuthenticationTokenError

security = HTTPBearer()


def get_current_user(
    request: Request,
    # credentials: HTTPAuthorizationCredentials = Depends(security),
):
    # token = credentials.credentials
    token = request.cookies.get( "access_token" )
    if token is None:
        raise AccessTokenMissingError()
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_aud": False},
        )
    except JWTError as exc:
        print( "JWTError: ", exc )
        raise InvalidAuthenticationTokenError() from exc

    user_id = payload.get("user_id")
    user_roles = payload.get("user_roles")

    if user_id is None or user_roles is None:
        print( "Invalid token payload" )
        raise InvalidAuthenticationTokenError("Invalid token payload")
    return {
        "user_id": user_id,
        "user_roles": user_roles,
    }
