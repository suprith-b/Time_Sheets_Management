from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(
    prefix = "/user"
)

@router.post( "" )
def create_user(
    db: Session = Depends( get_db )
):
    return UserService.create_user()

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