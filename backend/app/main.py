from fastapi import FastAPI

from app.core.config import settings
from app.db.database import get_db
from app.controllers.ProjectController import router as ProjectRouter
from app.controllers.TaskController import router as TaskRouter
from app.controllers.UserController import router as UserRouter

app = FastAPI()

app.include_router(UserRouter)
app.include_router(ProjectRouter)
app.include_router(TaskRouter)
