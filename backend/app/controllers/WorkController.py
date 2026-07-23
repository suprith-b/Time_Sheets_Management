from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import app.schemas.WorkSchema as WorkSchema
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.WorkModel import TypeEnum
from app.models.RoleModel import RoleEnum
from app.services.WorkService import WorkService


router = APIRouter(prefix="/work")


@router.get("/reports")
def get_work_reports(
    roles: list[RoleEnum] = Query(
        default_factory=lambda: [RoleEnum.MANAGER, RoleEnum.EMPLOYEE]
    ),
    project_ids: Optional[list[int]] = Query(default=None),
    sort_by: str = "duration",
    sort_type: int = Query(default=-1),
    types: list[TypeEnum] = Query(default_factory=lambda: list(TypeEnum)),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["user_role"] not in {"admin", "manager"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view work reports",
        )
    return WorkService.get_reports(
        current_user,
        roles,
        project_ids,
        sort_by,
        sort_type,
        types,
        start_time,
        end_time,
        db,
    )


@router.post("/{user_id}")
def create_works(
    user_id: int,
    works_data: list[WorkSchema.CreateWork],
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["user_role"] != "admin" and user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create work records for yourself",
        )
    return WorkService.create_works(user_id, works_data, db)


@router.patch("/{work_id}")
def edit_work(
    work_id: int,
    data: WorkSchema.EditWork,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["user_role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to edit work records",
        )
    return WorkService.edit_work(work_id, data, db)


@router.delete("/{work_id}")
def delete_work(
    work_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["user_role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete work records",
        )
    return WorkService.delete_work(work_id, db)


@router.get("/{user_id}")
def get_works(
    user_id: int,
    project_ids: Optional[list[int]] = Query(default=None),
    sort_by: str = "start_time",
    sort_type: int = Query(default=1),
    types: list[TypeEnum] = Query(default_factory=lambda: list(TypeEnum)),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return WorkService.get_works(
        user_id,
        current_user,
        project_ids,
        sort_by,
        sort_type,
        types,
        start_time,
        end_time,
        db,
    )

