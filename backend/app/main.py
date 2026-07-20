from fastapi import FastAPI

from app.core.config import settings
from app.db.database import get_db

app = FastAPI()

try:
    get_db()
    print( "connected to db" )
except Exception as e:
    print( str( e ) )