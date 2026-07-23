from fastapi import FastAPI

from app.core.config import settings
from app.db.database import get_db
from app.controllers.ProjectController import router as ProjectRouter
from app.controllers.TaskController import router as TaskRouter
from app.controllers.UserController import router as UserRouter
from app.controllers.WorkController import router as WorkRouter

app = FastAPI()
