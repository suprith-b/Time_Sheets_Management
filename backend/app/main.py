from fastapi import FastAPI

from app.core.config import settings
from app.db.database import get_db
from app.controllers.UserController import router as UserRouter

app = FastAPI()

app.include_router(UserRouter)
