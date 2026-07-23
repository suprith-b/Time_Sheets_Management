from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from app.core.config import settings
from app.db.database import Base, SessionLocal, engine, get_db
from app.controllers.AdminController import router as admin_router
from app.models.ManagerAssignmentModel import ManagerAssignment
from app.models.ProjectAssignmentModel import ProjectAssignment
from app.models.ProjectModel import Project
from app.models.RoleModel import Role, RoleEnum
from app.models.TaskModel import Task
from app.models.UserModel import User
from app.models.WorkModel import Work

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(admin_router)


@app.on_event("startup")
def prepare_database():
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    users_columns = {column["name"] for column in inspector.get_columns("users")}
    projects_columns = {column["name"] for column in inspector.get_columns("projects")}
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE roles MODIFY COLUMN role ENUM('employee', 'manager', 'admin')"))
        if "status" not in users_columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'active'"))
        if "active_status" not in projects_columns:
            connection.execute(text("ALTER TABLE projects ADD COLUMN active_status VARCHAR(20) NOT NULL DEFAULT 'active'"))
        if "project_image" not in projects_columns:
            connection.execute(text("ALTER TABLE projects ADD COLUMN project_image TEXT"))
    db = SessionLocal()
    try:
        existing_roles = {role.role for role in db.query(Role).all()}
        for role in RoleEnum:
            if role not in existing_roles:
                db.add(Role(role=role))
        db.commit()
    finally:
        db.close()

