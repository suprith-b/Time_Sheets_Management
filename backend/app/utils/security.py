from app.core.config import settings
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
import os
from datetime import datetime, timedelta, UTC
from jose import jwt
password_hash = PasswordHash((BcryptHasher(),))


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

# def create 
def create_access_token( user_details: dict ) -> str:
    payload = {}
    payload[ "user_id" ] = user_details.id
    payload[ "user_userid" ] = user_details.userid
    payload[ "user_roles" ] = user_details.roles
    payload[ "exp" ] = (datetime.now(UTC) + timedelta(days = 1)).timestamp()
    return create_JWT_token( payload )

def create_refresh_token( user_id: int ) -> str:
    payload = { "user_id" : user_id }
    payload[ "exp" ] = ( datetime.now(UTC) + timedelta(days=1) ).timestamp()
    return create_JWT_token( payload )

def create_JWT_token( data: dict ) -> str:
    # print( "algo: ", Settings.JWT_ALGORITHM)
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM )