"""Read-only data used by the admin dashboard."""

from collections import defaultdict
import base64
from datetime import date, datetime, timedelta, timezone
import hashlib
import hmac
import os

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import delete, func, or_, select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.ManagerAssignmentModel import ManagerAssignment
from app.models.ProjectAssignmentModel import ProjectAssignment
from app.models.ProjectModel import Project, StatusEnum
from app.models.RoleModel import Role, RoleEnum
from app.models.TaskModel import Task
from app.models.UserModel import User
from app.models.WorkModel import Work
from app.models.WorkModel import TypeEnum
from app.schemas.AdminEmployeeSchema import (
    EmployeeCreateRequest,
    EmployeeUpdateRequest,
    ManagerAssignmentRequest,
    ProjectAssignmentRequest,
)
from app.schemas.AdminProfileSchema import PasswordChangeRequest
from app.schemas.AdminProjectSchema import (
    ProjectCreateRequest,
    ProjectManagerRequest,
    ProjectUpdateRequest,
    TaskCreateRequest,
    TaskUpdateRequest,
)
from app.schemas.EmployeeTimesheetSchema import TimesheetSubmitRequest

router = APIRouter(prefix="/api/admin", tags=["admin"])


def _work_hours(work: Work) -> float:
    """Return a work record's duration in hours; incomplete records count as zero."""
    if not work.start_time or not work.end_time:
        return 0.0
    return max(0.0, (work.end_time - work.start_time).total_seconds() / 3600)


def _password_hash(password: str) -> str:
    """Create a PBKDF2 hash that fits the existing VARCHAR(60) column."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000, dklen=20)
    return "1$" + base64.b64encode(salt + digest).decode("ascii")


def _password_matches(password: str, stored_hash: str) -> bool:
    """Verify hashes created by _password_hash without exposing password data."""
    try:
        version, payload = stored_hash.split("$", maxsplit=1)
        raw = base64.b64decode(payload.encode("ascii"), validate=True)
        if version != "1" or len(raw) != 36:
            return False
        expected = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), raw[:16], 120_000, dklen=20)
        return hmac.compare_digest(expected, raw[16:])
    except (ValueError, TypeError):
        return False


def _role_id(db: Session, role: RoleEnum) -> int:
    role_record = db.scalar(select(Role).where(Role.role == role))
    if role_record is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The '{role.value}' role has not been seeded in the Roles table.",
        )
    return role_record.id


def _get_user(db: Session, employee_id: int) -> User:
    user = db.get(User, employee_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")
    return user


def _validate_manager(db: Session, employee_id: int, manager_id: int) -> None:
    if employee_id == manager_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="A user cannot manage themselves.")
    manager = _get_user(db, manager_id)
    manager_role = db.get(Role, manager.role_id)
    if manager_role is None or manager_role.role != RoleEnum.MANAGER:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="manager_id must belong to a manager.")


def _replace_manager(db: Session, employee_id: int, manager_id: int | None) -> None:
    if manager_id is not None:
        _validate_manager(db, employee_id, manager_id)
    db.execute(delete(ManagerAssignment).where(ManagerAssignment.employee_id == employee_id))
    if manager_id is not None:
        db.add(ManagerAssignment(employee_id=employee_id, manager_id=manager_id))


def _validate_project_ids(db: Session, project_ids: list[int]) -> list[int]:
    unique_ids = list(dict.fromkeys(project_ids))
    projects = list(db.scalars(select(Project).where(Project.id.in_(unique_ids)))) if unique_ids else []
    found_ids = {project.id for project in projects}
    missing_ids = sorted(set(unique_ids) - found_ids)
    if missing_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project IDs not found: {missing_ids}")
    return unique_ids


def _replace_projects(db: Session, employee_id: int, project_ids: list[int]) -> None:
    project_ids = _validate_project_ids(db, project_ids)
    db.execute(delete(ProjectAssignment).where(ProjectAssignment.user_id == employee_id))
    db.add_all([ProjectAssignment(user_id=employee_id, project_id=project_id) for project_id in project_ids])


def _employee_response(db: Session, user: User) -> dict:
    role = db.get(Role, user.role_id)
    manager_assignment = db.scalar(
        select(ManagerAssignment).where(ManagerAssignment.employee_id == user.id)
    )
    manager = db.get(User, manager_assignment.manager_id) if manager_assignment else None
    projects = list(
        db.execute(
            select(Project.id, Project.name)
            .join(ProjectAssignment, ProjectAssignment.project_id == Project.id)
            .where(ProjectAssignment.user_id == user.id)
            .order_by(Project.name)
        )
    )
    return {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "role": role.role.value if role else None,
        "status": getattr(user, "status", None) or "active",
        "manager": None if manager is None else {"id": manager.id, "name": manager.name, "email": manager.email},
        "projects": [{"id": project_id, "name": project_name} for project_id, project_name in projects],
    }


def _get_project(db: Session, project_id: int) -> Project:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    return project


def _get_task(db: Session, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return task


def _validate_project_manager(db: Session, manager_id: int) -> User:
    manager = _get_user(db, manager_id)
    role = db.get(Role, manager.role_id)
    if role is None or role.role != RoleEnum.MANAGER:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="manager_id must belong to a manager.")
    return manager


def _replace_project_manager(db: Session, project_id: int, manager_id: int | None) -> None:
    if manager_id is not None:
        _validate_project_manager(db, manager_id)
    manager_user_ids = select(User.id).join(Role, User.role_id == Role.id).where(Role.role == RoleEnum.MANAGER)
    db.execute(
        delete(ProjectAssignment).where(
            ProjectAssignment.project_id == project_id,
            ProjectAssignment.user_id.in_(manager_user_ids),
        )
    )
    if manager_id is not None:
        already_assigned = db.scalar(
            select(ProjectAssignment).where(
                ProjectAssignment.project_id == project_id,
                ProjectAssignment.user_id == manager_id,
            )
        )
        if already_assigned is None:
            db.add(ProjectAssignment(project_id=project_id, user_id=manager_id))


def _project_response(db: Session, project: Project) -> dict:
    manager = db.scalar(
        select(User)
        .join(ProjectAssignment, ProjectAssignment.user_id == User.id)
        .join(Role, User.role_id == Role.id)
        .where(ProjectAssignment.project_id == project.id, Role.role == RoleEnum.MANAGER)
        .order_by(User.name)
    )
    task_count = db.scalar(select(func.count(Task.id)).where(Task.project_id == project.id)) or 0
    works = db.scalars(
        select(Work).join(Task, Work.task_id == Task.id).where(Task.project_id == project.id)
    )
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "start_date": project.start_date,
        "end_date": project.end_date,
        "status": project.status.value,
        "active_status": getattr(project, "active_status", None) or "active",
        "project_image": getattr(project, "project_image", None),
        "manager": None if manager is None else {"id": manager.id, "name": manager.name},
        "task_count": task_count,
        "hours_logged": round(sum(_work_hours(work) for work in works), 2),
    }


def _task_response(task: Task) -> dict:
    return {"id": task.id, "project_id": task.project_id, "name": task.name, "description": task.description}


def _employee_project_response(db: Session, user: User) -> dict:
    projects = list(
        db.scalars(
            select(Project)
            .join(ProjectAssignment, ProjectAssignment.project_id == Project.id)
            .where(ProjectAssignment.user_id == user.id)
            .order_by(Project.name)
        )
    )
    tasks_by_project = defaultdict(list)
    if projects:
        project_ids = [project.id for project in projects]
        for task in db.scalars(select(Task).where(Task.project_id.in_(project_ids)).order_by(Task.name)):
            tasks_by_project[task.project_id].append(_task_response(task))
    return {
        "employee": _employee_response(db, user),
        "projects": [
            {
                **_project_response(db, project),
                "tasks": tasks_by_project[project.id],
            }
            for project in projects
        ],
    }


@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    """Return aggregate information the current database can support for admins.

    Authentication/role enforcement will be added with the auth module. This endpoint
    deliberately does not fabricate approval or activity data, because those fields
    are not stored in the current schema.
    """
    users = list(db.scalars(select(User)))
    roles = {role.id: role.role.value for role in db.scalars(select(Role))}
    projects = list(db.scalars(select(Project)))
    assignments = list(db.scalars(select(ProjectAssignment)))
    manager_assignments = list(db.scalars(select(ManagerAssignment)))
    tasks = list(db.scalars(select(Task)))
    works = list(db.scalars(select(Work)))

    employee_ids = {user.id for user in users if roles.get(user.role_id) == RoleEnum.EMPLOYEE.value}
    project_members = defaultdict(set)
    for assignment in assignments:
        if assignment.user_id in employee_ids:
            project_members[assignment.project_id].add(assignment.user_id)

    task_projects = {task.id: task.project_id for task in tasks}
    project_task_counts = defaultdict(int)
    for task in tasks:
        project_task_counts[task.project_id] += 1
    project_hours = defaultdict(float)
    user_hours = defaultdict(float)
    for work in works:
        hours = _work_hours(work)
        user_hours[work.user_id] += hours
        project_id = task_projects.get(work.task_id)
        if project_id is not None:
            project_hours[project_id] += hours

    managers = [user for user in users if roles.get(user.role_id) == RoleEnum.MANAGER.value]
    employees = [user for user in users if user.id in employee_ids]
    team_members = defaultdict(set)
    for assignment in manager_assignments:
        team_members[assignment.manager_id].add(assignment.employee_id)

    today = date.today()
    upcoming_deadline = today + timedelta(days=7)
    unassigned_employee_count = sum(
        1 for employee in employees if not any(employee.id in members for members in project_members.values())
    )

    return {
        "generated_at": datetime.now(timezone.utc),
        "statistics": {
            "total_users": len(users),
            "total_employees": len(employees),
            "total_managers": len(managers),
            "active_projects": sum((getattr(project, "active_status", None) or "active") == "active" for project in projects),
            "total_projects": len(projects),
            "hours_logged": round(sum(_work_hours(work) for work in works), 2),
            "pending_timesheets": None,
        },
        "projects": [
            {
                "id": project.id,
                "name": project.name,
                "status": project.status.value,
                "active_status": getattr(project, "active_status", None) or "active",
                "project_image": getattr(project, "project_image", None),
                "start_date": project.start_date,
                "end_date": project.end_date,
                "assigned_employee_count": len(project_members[project.id]),
                "task_count": project_task_counts[project.id],
                "hours_logged": round(project_hours[project.id], 2),
            }
            for project in projects
        ],
        "team_workload": [
            {
                "manager_id": manager.id,
                "manager_name": manager.name,
                "team_size": len(team_members[manager.id]),
                "hours_logged": round(sum(user_hours[employee_id] for employee_id in team_members[manager.id]), 2),
            }
            for manager in managers
        ],
        "attention": {
            "unassigned_employees": unassigned_employee_count,
            "projects_due_within_seven_days": sum(
                project.end_date is not None
                and today <= project.end_date <= upcoming_deadline
                and project.status != StatusEnum.COMPLETED
                for project in projects
            ),
            "pending_timesheets": None,
        },
        "recent_activity": [],
    }


@router.get("/employee/context")
def get_employee_context(user_id: int | None = None, db: Session = Depends(get_db)):
    """Return the active employee and their assigned projects/tasks."""
    if user_id is None:
        user = db.scalar(
            select(User)
            .join(Role, User.role_id == Role.id)
            .where(Role.role == RoleEnum.EMPLOYEE)
            .order_by(User.id)
        )
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No employee user exists yet.")
    else:
        user = _get_user(db, user_id)
        role = db.get(Role, user.role_id)
        if role is None or role.role != RoleEnum.EMPLOYEE:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="user_id must belong to an employee.")
    return _employee_project_response(db, user)


@router.get("/manager/context")
def get_manager_context(user_id: int | None = None, db: Session = Depends(get_db)):
    """Return the active manager and their assigned projects/tasks."""
    if user_id is None:
        user = db.scalar(
            select(User)
            .join(Role, User.role_id == Role.id)
            .where(Role.role == RoleEnum.MANAGER)
            .order_by(User.id)
        )
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No manager user exists yet.")
    else:
        user = _get_user(db, user_id)
        role = db.get(Role, user.role_id)
        if role is None or role.role != RoleEnum.MANAGER:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="user_id must belong to a manager.")
    return _employee_project_response(db, user)


@router.post("/employee/timesheets", status_code=status.HTTP_201_CREATED)
def submit_employee_timesheet(payload: TimesheetSubmitRequest, db: Session = Depends(get_db)):
    """Create work rows submitted from the employee timesheet screen."""
    user = _get_user(db, payload.user_id)
    role = db.get(Role, user.role_id)
    if role is None or role.role != RoleEnum.EMPLOYEE:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Only employees can submit timesheets.")

    assigned_project_ids = {
        assignment.project_id
        for assignment in db.scalars(select(ProjectAssignment).where(ProjectAssignment.user_id == user.id))
    }
    task_ids = [entry.task_id for entry in payload.entries]
    tasks = {task.id: task for task in db.scalars(select(Task).where(Task.id.in_(task_ids)))}
    missing_task_ids = sorted(set(task_ids) - set(tasks))
    if missing_task_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task IDs not found: {missing_task_ids}")
    invalid_task_ids = sorted(task_id for task_id, task in tasks.items() if task.project_id not in assigned_project_ids)
    if invalid_task_ids:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Tasks are not assigned to this employee: {invalid_task_ids}")

    work_rows = [
        Work(
            user_id=user.id,
            task_id=entry.task_id,
            start_time=datetime.combine(entry.work_date, entry.start_time),
            end_time=datetime.combine(entry.work_date, entry.end_time),
            comments=entry.comments,
            type=entry.type,
        )
        for entry in payload.entries
    ]
    db.add_all(work_rows)
    db.commit()
    return {"created": len(work_rows)}


@router.post("/manager/timesheets", status_code=status.HTTP_201_CREATED)
def submit_manager_timesheet(payload: TimesheetSubmitRequest, db: Session = Depends(get_db)):
    """Create work rows submitted from the manager timesheet screen."""
    user = _get_user(db, payload.user_id)
    role = db.get(Role, user.role_id)
    if role is None or role.role != RoleEnum.MANAGER:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Only managers can submit timesheets.")

    assigned_project_ids = {
        assignment.project_id
        for assignment in db.scalars(select(ProjectAssignment).where(ProjectAssignment.user_id == user.id))
    }
    task_ids = [entry.task_id for entry in payload.entries]
    tasks = {task.id: task for task in db.scalars(select(Task).where(Task.id.in_(task_ids)))}
    missing_task_ids = sorted(set(task_ids) - set(tasks))
    if missing_task_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task IDs not found: {missing_task_ids}")
    invalid_task_ids = sorted(task_id for task_id, task in tasks.items() if task.project_id not in assigned_project_ids)
    if invalid_task_ids:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Tasks are not assigned to this manager: {invalid_task_ids}")

    work_rows = [
        Work(
            user_id=user.id,
            task_id=entry.task_id,
            start_time=datetime.combine(entry.work_date, entry.start_time),
            end_time=datetime.combine(entry.work_date, entry.end_time),
            comments=entry.comments,
            type=entry.type,
        )
        for entry in payload.entries
    ]
    db.add_all(work_rows)
    db.commit()
    return {"created": len(work_rows)}


@router.get("/employees")
def list_employees(
    role: RoleEnum | None = Query(default=None),
    db: Session = Depends(get_db),
):
    """List users for the Admin Manage Employees table, optionally by role."""
    statement = select(User).join(Role, User.role_id == Role.id).order_by(User.name)
    if role is not None:
        statement = statement.where(Role.role == role)
    return [_employee_response(db, user) for user in db.scalars(statement)]


@router.post("/employees", status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreateRequest, db: Session = Depends(get_db)):
    """Create a user, then optionally assign one manager and projects."""
    duplicate = db.scalar(select(User).where((User.email == payload.email) | (User.username == payload.username)))
    if duplicate is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or username is already in use.")

    role_id = _role_id(db, payload.role)
    user = User(
        username=payload.username,
        name=payload.name,
        email=payload.email,
        password=_password_hash(payload.password),
        role_id=role_id,
        status=payload.status,
    )
    db.add(user)
    db.flush()

    if payload.manager_id is not None:
        _replace_manager(db, user.id, payload.manager_id)
    if payload.project_ids:
        _replace_projects(db, user.id, payload.project_ids)
    db.commit()
    db.refresh(user)
    return _employee_response(db, user)


@router.put("/employees/{employee_id}")
def update_employee(employee_id: int, payload: EmployeeUpdateRequest, db: Session = Depends(get_db)):
    """Update basic employee data and/or their role."""
    user = _get_user(db, employee_id)
    changes = payload.model_dump(exclude_unset=True)
    if "email" in changes or "username" in changes:
        duplicate_query = select(User).where(User.id != employee_id)
        duplicate_conditions = []
        if "email" in changes:
            duplicate_conditions.append(User.email == changes["email"])
        if "username" in changes:
            duplicate_conditions.append(User.username == changes["username"])
        duplicate_query = duplicate_query.where(or_(*duplicate_conditions))
        if db.scalar(duplicate_query) is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or username is already in use.")

    for field in ("username", "name", "email", "status"):
        if field in changes:
            setattr(user, field, changes[field])
    if "role" in changes:
        user.role_id = _role_id(db, changes["role"])
        if changes["role"] != RoleEnum.EMPLOYEE:
            _replace_manager(db, employee_id, None)
    db.commit()
    db.refresh(user)
    return _employee_response(db, user)


@router.put("/employees/{employee_id}/manager")
def assign_manager(employee_id: int, payload: ManagerAssignmentRequest, db: Session = Depends(get_db)):
    """Set or clear an employee's manager assignment."""
    user = _get_user(db, employee_id)
    user_role = db.get(Role, user.role_id)
    if user_role is None or user_role.role != RoleEnum.EMPLOYEE:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Only employees can have a manager assignment.")
    _replace_manager(db, employee_id, payload.manager_id)
    db.commit()
    return _employee_response(db, user)


@router.put("/employees/{employee_id}/projects")
def assign_projects(employee_id: int, payload: ProjectAssignmentRequest, db: Session = Depends(get_db)):
    """Replace a user's project assignments with the selected project IDs."""
    user = _get_user(db, employee_id)
    _replace_projects(db, employee_id, payload.project_ids)
    db.commit()
    return _employee_response(db, user)


@router.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Remove a user only when doing so will not erase their submitted work history."""
    user = _get_user(db, employee_id)
    has_work = db.scalar(select(Work.id).where(Work.user_id == employee_id).limit(1))
    if has_work is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee has work history. Preserve it by reassigning or deleting the work records first.",
        )
    db.execute(delete(ProjectAssignment).where(ProjectAssignment.user_id == employee_id))
    db.execute(
        delete(ManagerAssignment).where(
            (ManagerAssignment.employee_id == employee_id) | (ManagerAssignment.manager_id == employee_id)
        )
    )
    db.delete(user)
    db.commit()


@router.get("/projects")
def list_projects(
    status_filter: StatusEnum | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
):
    """List projects with the manager, task count, and work hours used by the admin table."""
    statement = select(Project).order_by(Project.start_date.desc(), Project.name)
    if status_filter is not None:
        statement = statement.where(Project.status == status_filter)
    return [_project_response(db, project) for project in db.scalars(statement)]


@router.post("/projects", status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreateRequest, db: Session = Depends(get_db)):
    project = Project(
        name=payload.name,
        description=payload.description,
        start_date=payload.start_date,
        end_date=payload.end_date,
        status=payload.status,
        active_status=payload.active_status,
        project_image=payload.project_image,
    )
    db.add(project)
    db.flush()
    if payload.manager_id is not None:
        _replace_project_manager(db, project.id, payload.manager_id)
    db.commit()
    db.refresh(project)
    return _project_response(db, project)


@router.put("/projects/{project_id}")
def update_project(project_id: int, payload: ProjectUpdateRequest, db: Session = Depends(get_db)):
    project = _get_project(db, project_id)
    changes = payload.model_dump(exclude_unset=True)
    start_date = changes.get("start_date", project.start_date)
    end_date = changes.get("end_date", project.end_date)
    if start_date is not None and end_date is not None and end_date < start_date:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="end_date must be on or after start_date.")
    for field, value in changes.items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return _project_response(db, project)


@router.put("/projects/{project_id}/manager")
def assign_project_manager(project_id: int, payload: ProjectManagerRequest, db: Session = Depends(get_db)):
    project = _get_project(db, project_id)
    _replace_project_manager(db, project.id, payload.manager_id)
    db.commit()
    return _project_response(db, project)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete only empty projects, preserving tasks and submitted work history."""
    project = _get_project(db, project_id)
    if db.scalar(select(Task.id).where(Task.project_id == project_id).limit(1)) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project has tasks. Delete or move its tasks before deleting the project.",
        )
    db.execute(delete(ProjectAssignment).where(ProjectAssignment.project_id == project_id))
    db.delete(project)
    db.commit()


@router.get("/projects/{project_id}/tasks")
def list_project_tasks(project_id: int, db: Session = Depends(get_db)):
    _get_project(db, project_id)
    tasks = db.scalars(select(Task).where(Task.project_id == project_id).order_by(Task.name))
    return [_task_response(task) for task in tasks]


@router.post("/projects/{project_id}/tasks", status_code=status.HTTP_201_CREATED)
def create_task(project_id: int, payload: TaskCreateRequest, db: Session = Depends(get_db)):
    _get_project(db, project_id)
    task = Task(project_id=project_id, name=payload.name, description=payload.description)
    db.add(task)
    db.commit()
    db.refresh(task)
    return _task_response(task)


@router.put("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdateRequest, db: Session = Depends(get_db)):
    task = _get_task(db, task_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return _task_response(task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = _get_task(db, task_id)
    if db.scalar(select(Work.id).where(Work.task_id == task.id).limit(1)) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task has submitted work. Delete or move the work records first.",
        )
    db.delete(task)
    db.commit()


@router.get("/profile/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    """Get profile data. Authentication will later restrict this to the current user."""
    user = _get_user(db, user_id)
    role = db.get(Role, user.role_id)
    return {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "role": role.role.value if role else None,
    }


@router.patch("/profile/{user_id}/password", status_code=status.HTTP_204_NO_CONTENT)
def change_profile_password(user_id: int, payload: PasswordChangeRequest, db: Session = Depends(get_db)):
    user = _get_user(db, user_id)
    if not _password_matches(payload.current_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect.")
    user.password = _password_hash(payload.new_password)
    db.commit()


@router.get("/reports")
def get_reports(
    project_id: list[int] | None = Query(default=None),
    work_type: TypeEnum | None = Query(default=None, alias="type"),
    role: RoleEnum | None = Query(default=None),
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    """Group work hours by employee and project for the Reports screen."""
    statement = (
        select(Work, User, Role, Task, Project)
        .join(User, Work.user_id == User.id)
        .join(Role, User.role_id == Role.id)
        .join(Task, Work.task_id == Task.id)
        .join(Project, Task.project_id == Project.id)
    )
    if project_id:
        statement = statement.where(Project.id.in_(project_id))
    if work_type is not None:
        statement = statement.where(Work.type == work_type)
    if role is not None:
        statement = statement.where(Role.role == role)
    if start_date is not None:
        statement = statement.where(Work.start_time >= datetime.combine(start_date, datetime.min.time()))
    if end_date is not None:
        statement = statement.where(Work.end_time < datetime.combine(end_date + timedelta(days=1), datetime.min.time()))

    grouped = defaultdict(float)
    for work, user, user_role, task, project in db.execute(statement):
        grouped[(user.id, user.name, user_role.role.value, project.id, project.name)] += _work_hours(work)
    return [
        {
            "employee_id": employee_id,
            "employee_name": employee_name,
            "role": role_name,
            "project_id": grouped_project_id,
            "project_name": project_name,
            "hours_logged": round(hours, 2),
        }
        for (employee_id, employee_name, role_name, grouped_project_id, project_name), hours in sorted(
            grouped.items(), key=lambda item: (item[0][1], item[0][4])
        )
    ]


@router.get("/history/{employee_id}")
def get_employee_history(
    employee_id: int,
    project_id: list[int] | None = Query(default=None),
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    """Return the individual work entries behind a report row."""
    _get_user(db, employee_id)
    statement = (
        select(Work, Task, Project)
        .join(Task, Work.task_id == Task.id)
        .join(Project, Task.project_id == Project.id)
        .where(Work.user_id == employee_id)
        .order_by(Work.start_time.desc())
    )
    if project_id:
        statement = statement.where(Project.id.in_(project_id))
    if start_date is not None:
        statement = statement.where(Work.start_time >= datetime.combine(start_date, datetime.min.time()))
    if end_date is not None:
        statement = statement.where(Work.end_time < datetime.combine(end_date + timedelta(days=1), datetime.min.time()))
    return [
        {
            "work_id": work.id,
            "project_id": project.id,
            "project_name": project.name,
            "task_id": task.id,
            "task_name": task.name,
            "start_time": work.start_time,
            "end_time": work.end_time,
            "duration_hours": round(_work_hours(work), 2),
            "comments": work.comments,
            "type": work.type.value,
        }
        for work, task, project in db.execute(statement)
    ]
