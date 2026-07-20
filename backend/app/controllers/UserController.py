from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
import app.schemas.UserSchema as UserSchema
from app.services.UserService import UserService

router = APIRouter(
    prefix = "/user"
)


@router.get( "" )
def get_users(
    db: Session = Depends( get_db )
):
    return UserService.get_users()

@router.get( "/{user_id}" )
def get_user(
    user_id: int,
    db: Session = Depends( get_db )
):
    return UserService.get_user( user_id )

@router.post( "" )
def create_user(
    data: UserSchema.CreateUser,
    db: Session = Depends( get_db )
):
    return UserService.create_user( data, db )

@router.delete( "/{user_id}" )
def delete_user( 
    user_id: int,
    db: Session = Depends( get_db ) 
):
    return UserService.delete_user( user_id )

@router.patch( "/{user_id}" )
def edit_user(
    user_id: int,
    db: Session = Depends( get_db )
):
    return UserService.edit_user( user_id )