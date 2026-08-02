from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.AnalyticsController import router as analytics_router
from app.controllers.AssignmentController import router as assignment_router
from app.controllers.AuthController import router as auth_router
from app.controllers.ProjectController import router as project_router
from app.controllers.TaskController import router as task_router
from app.controllers.TimeLogController import router as timelog_router
from app.controllers.UserController import router as user_router

app = FastAPI(title="Timesheets V2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(assignment_router)
app.include_router(timelog_router)
app.include_router(analytics_router)