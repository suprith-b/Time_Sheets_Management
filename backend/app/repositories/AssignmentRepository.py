from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_, insert

from app.models.ProjectAssignmentModel import ProjectAssignment
from app.models.RoleAssignmentModel import RoleAssignment
from app.models.RoleModel import Role, RoleEnum
from app.models.UserModel import User


class AssignmentRepository:
    @staticmethod
    def get_role_id_map(role_enums: list[RoleEnum], db: Session) -> dict[RoleEnum, int]:
        if not role_enums:
            return {}
        rows = db.query(Role.id, Role.role).filter(Role.role.in_(role_enums)).all()
        return {row.role: row.id for row in rows}

    @staticmethod
    def get_project_assignment_map(user_id: int, db: Session) -> dict[int, ProjectAssignment]:
        rows = db.query(ProjectAssignment).filter(ProjectAssignment.user_id == user_id).all()
        return {row.project_id: row for row in rows}

    @staticmethod
    def get_role_assignment_map(user_id: int, db: Session) -> dict[int, RoleAssignment]:
        rows = db.query(RoleAssignment).filter(RoleAssignment.user_id == user_id).all()
        return {row.role_id: row for row in rows}

    @staticmethod
    def sync_user_roles(user_id: int, roles: list[RoleEnum], db: Session) -> None:
        role_id_map = AssignmentRepository.get_role_id_map(roles, db)
        existing = AssignmentRepository.get_role_assignment_map(user_id, db)

        desired_role_ids = set(role_id_map.values())
        for role_id, assignment in existing.items():
            assignment.is_assigned = role_id in desired_role_ids

        missing = [
            {"user_id": user_id, "role_id": role_id, "is_assigned": True}
            for role_id in desired_role_ids
            if role_id not in existing.keys()
        ]
        if missing:
            db.execute(insert(RoleAssignment).values(missing))
        db.commit()

    @staticmethod
    def add_user_roles(user_ids: list[int], roles: list[RoleEnum], db: Session) -> None:
        if not user_ids or not roles:
            return

        role_id_map = AssignmentRepository.get_role_id_map(roles, db)
        existing_rows = (
            db.query(RoleAssignment)
            .filter(RoleAssignment.user_id.in_(user_ids), RoleAssignment.is_assigned)
            .all()
        )
        existing_map = {(row.user_id, row.role_id): row for row in existing_rows}
        desired_pairs = {(user_id, role_id) for user_id in user_ids for role_id in role_id_map.values()}

        for (user_id, role_id), assignment in existing_map.items():
            assignment.is_assigned = (user_id, role_id) in desired_pairs

        missing = [
            {"user_id": user_id, "role_id": role_id, "is_assigned": True}
            for user_id in user_ids
            for role_id in role_id_map.values()
            if (user_id, role_id) not in existing_map
        ]
        if missing:
            db.execute(insert(RoleAssignment).values(missing))
        db.commit()

    @staticmethod
    def revoke_users_roles(user_ids: list[int], roles: list[RoleEnum], db: Session) -> None:
        if not user_ids or not roles:
            return

        role_id_map = AssignmentRepository.get_role_id_map(roles, db)
        rows = (
            db.query(RoleAssignment)
            .filter(RoleAssignment.user_id.in_(user_ids), RoleAssignment.role_id.in_(list(role_id_map.values())))
            .all()
        )
        for row in rows:
            row.is_assigned = False
        db.commit()

    @staticmethod
    def add_projects_to_user(user_id: int, project_ids: list[int], current_user: dict, db: Session) -> None:
        if not project_ids:
            return

        existing_rows = (
            db.query(ProjectAssignment)
            .filter(ProjectAssignment.user_id == user_id)
            .all()
        )
        existing_project_ids = {row.project_id for row in existing_rows}

        for row in existing_rows:
            row.is_assigned = True

        missing = [
            {"user_id": user_id, "project_id": project_id, "is_assigned": True}
            for project_id in project_ids
            if project_id not in existing_project_ids
        ]
        if missing:
            db.execute(insert(ProjectAssignment).values(missing))
        db.commit()

    @staticmethod
    def revoke_projects_from_user(user_id: int, project_ids: list[int], current_user: dict, db: Session) -> None:
        if not project_ids:
            return
        
        db.query(ProjectAssignment).filter(
            ProjectAssignment.user_id == user_id,
            ProjectAssignment.project_id.in_(project_ids)
        ).update({"is_assigned": False}, synchronize_session=False)
        db.commit()

    @staticmethod
    def revoke_users_from_project(project_id: int, user_ids: list[int], db: Session) -> None:
        if not user_ids:
            return

        db.query(ProjectAssignment).filter(
            ProjectAssignment.project_id == project_id,
            ProjectAssignment.user_id.in_(user_ids)
        ).update({"is_assigned": False}, synchronize_session=False)
        db.commit()

    @staticmethod
    def add_users_to_projects(project_id: int, user_ids: list[int], db: Session) -> None:
        if not user_ids:
            return

        existing_rows = (
            db.query(ProjectAssignment)
            .filter(ProjectAssignment.project_id == project_id)
            .all()
        )
        existing_user_ids = {row.user_id for row in existing_rows}
        for row in existing_rows:
            row.is_assigned = True
        missing = [
            {"user_id": user_id, "project_id": project_id, "is_assigned": True}
            for user_id in user_ids
            if user_id not in existing_user_ids
        ]
        if missing:
            db.execute(insert(ProjectAssignment).values(missing))
        db.commit()

    @staticmethod
    def are_users_managed_by(manager_id: int, user_ids: list[int], db: Session) -> bool:
        if not user_ids:
            return True
        managed_count = (
            db.query(User.id)
            .filter(User.id.in_(user_ids), User.manager_id == manager_id)
            .count()
        )
        return managed_count == len(set(user_ids))

    @staticmethod
    def can_view_users_projects(manager_id: int, user_ids: list[int], db: Session) -> bool:
        if not user_ids:
            return True

        ManagerAssignment = aliased(ProjectAssignment)
        UserAssignment = aliased(ProjectAssignment)

        managed_count = (
            db.query(User.id)
            .outerjoin(
                UserAssignment,
                and_(
                    UserAssignment.user_id == User.id,
                    UserAssignment.is_assigned.is_(True),
                ),
            )
            .outerjoin(
                ManagerAssignment,
                and_(
                    ManagerAssignment.project_id == UserAssignment.project_id,
                    ManagerAssignment.user_id == manager_id,
                    ManagerAssignment.is_assigned.is_(True),
                ),
            )
            .filter(
                User.id.in_(user_ids),
                or_(
                    User.manager_id == manager_id,
                    ManagerAssignment.user_id.isnot(None),
                ),
            )
            .distinct()
            .count()
        )

        return managed_count == len(set(user_ids))