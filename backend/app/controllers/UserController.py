from http.client import HTTPException

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
import app.schemas.UserSchema as UserSchema
from app.dependencies.auth import get_current_user
from app.services.UserService import UserService

router = APIRouter(
    prefix = "/user"
)


@router.get( "" )
def get_users(
    db: Session = Depends( get_db ),
    current_user: dict = Depends(get_current_user)
):
    if ( current_user["user_role"] != "admin" and current_user["user_role"] != "manager" ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return UserService.get_users( current_user, db )

@router.get( "/{user_id}" )
def get_user(
    user_id: int,
    db: Session = Depends( get_db ),
    current_user: dict = Depends(get_current_user)
):
    if ( current_user["user_role"] != "admin" and current_user["user_role"] != "manager" and current_user["user_id"] != user_id ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return UserService.get_user( current_user, user_id, db )

@router.post( "" )
def create_user(
    data: UserSchema.CreateUser,
    db: Session = Depends( get_db ),
    current_user: dict = Depends(get_current_user)
):
    if ( current_user["user_role"] != "admin" ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return UserService.create_user( data, db )

@router.delete( "/{user_id}" )
def delete_user( 
    user_id: int,
    db: Session = Depends( get_db ),
    current_user: dict = Depends(get_current_user)
):
    if ( current_user["user_role"] != "admin" ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return UserService.delete_user( user_id, db )

@router.patch( "/{user_id}" )
def edit_user(
    user_id: int,
    data: UserSchema.EditUser,
    db: Session = Depends( get_db ),
    current_user: dict = Depends(get_current_user)
):
    if ( current_user["user_role"] != "admin" and current_user["user_id"] != user_id ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return UserService.edit_user( user_id, data, db )
