from fastapi import status
from fastapi import HTTPException
from fastapi import Request
from fastapi import responses
from datetime import timedelta
from datetime import UTC
from datetime import datetime
from app.utils.security import create_access_token, create_refresh_token
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.db.database import get_db
import app.schemas.AuthSchema as AuthSchema
from app.services.AuthService import AuthService

router = APIRouter(prefix="/auth")

@router.post("/login")
def login(
    data: AuthSchema.LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    user_details = AuthService.login(data, db)

    access_token = create_access_token(user_details)
    refresh_token = create_refresh_token(user_details.id)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,      # False for local HTTP development
        samesite="lax",
        max_age=15 * 60,
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
    )
    return {"message": "Login successful"}

@router.post( "/refresh" )
def refresh(
    response: Response,
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("refresh_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing"
        )
    
    user_details = AuthService.refresh(token, db)
    if user_details is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid refresh token"
        )

    access_token = create_access_token( user_details )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age= 15 * 60
    )
    return {"message": "Token refreshed successfully"}

@router.post("/logout")
def logout(
    response: Response,
):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Logged out successfully"}

