from fastapi import FastAPI

from app.controllers.AnalyticsController import router as analytics_router
from app.controllers.AssignmentController import router as assignment_router
from app.controllers.AuthController import router as auth_router
from app.controllers.ProjectController import router as project_router
from app.controllers.TaskController import router as task_router
from app.controllers.TimeLogController import router as timelog_router
from app.controllers.UserController import router as user_router

app = FastAPI(title="Timesheets V2")
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(assignment_router)
app.include_router(timelog_router)
app.include_router(analytics_router)