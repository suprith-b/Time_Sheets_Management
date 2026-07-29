from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from app.models.ProjectAssignmentModel import ProjectAssignment
from app.models.RoleAssignmentModel import RoleAssignment
from app.models.RoleModel import Role, RoleEnum
from app.models.UserModel import User


class AssignmentRepository:

    @staticmethod
    def update_users_manager(manager_id: int, employee_ids: list[int], db: Session):
        if employee_ids:
            db.query(User).filter(User.id.in_(employee_ids)).update(
                {User.manager_id: manager_id}, synchronize_session=False
            )
            db.commit()

    @staticmethod
    def are_users_managed_by(manager_id: int, user_ids: list[int], db: Session) -> bool:
        if not user_ids:
            return True
        managed_count = (
            db.query(User.id)
            .filter(
                User.id.in_(user_ids),
                User.manager_id == manager_id
            )
            .count()
        )
        return managed_count == len(set(user_ids))

    @staticmethod
    def assign_projects(user_ids: list[int], project_ids: list[int], db: Session):
        if not user_ids or not project_ids:
            return

        db.query(ProjectAssignment).filter(
            ProjectAssignment.user_id.in_(user_ids),
            ProjectAssignment.project_id.in_(project_ids),
        ).update(
            {ProjectAssignment.is_assigned: True},
            synchronize_session=False,
        )

        existing_pairs = set(
            db.query(
                ProjectAssignment.user_id,
                ProjectAssignment.project_id,
            ).filter(
                ProjectAssignment.user_id.in_(user_ids),
                ProjectAssignment.project_id.in_(project_ids),
            ).all()
        )

        new_assignments = [
            {
                "user_id": u_id, 
                "project_id": p_id, 
                "is_assigned": True
            }
            for u_id in user_ids
            for p_id in project_ids
            if (u_id, p_id) not in existing_pairs
        ]
        if new_assignments:
            db.execute( insert(ProjectAssignment).values(new_assignments))
        db.commit()

    @staticmethod
    def deassign_projects(user_ids: list[int], project_ids: list[int], db: Session):
        if not user_ids or not project_ids:
            return

        db.query(ProjectAssignment).filter(
            ProjectAssignment.user_id.in_(user_ids),
            ProjectAssignment.project_id.in_(project_ids),
        ).update({ProjectAssignment.is_assigned: False}, synchronize_session=False)

        db.commit()

    @staticmethod
    def assign_roles(user_ids: list[int], roles: list[RoleEnum], db: Session):
        if not user_ids or not roles:
            return

        db_roles = db.query(Role).filter(Role.role.in_(roles)).all()
        role_ids = [ db_role.id for db_role in db_roles ]
        
        db.query(RoleAssignment).filter(
            RoleAssignment.user_id.in_(user_ids),
            RoleAssignment.role_id.in_(role_ids),
        ).update(
            {RoleAssignment.is_assigned: True},
            synchronize_session=False,
        )

        existing_pairs = set(
            db.query(
                RoleAssignment.user_id,
                RoleAssignment.role_id,
            ).filter(
                RoleAssignment.user_id.in_(user_ids),
                RoleAssignment.role_id.in_(role_ids),
            ).all()
        )
        new_assignments = [
            {
                "user_id": u_id, 
                "role_id": r_id, 
                "is_assigned": True
            }
            for u_id in user_ids
            for r_id in role_ids
            if (u_id, r_id) not in existing_pairs
        ]
        if new_assignments:
            db.execute( insert(RoleAssignment).values(new_assignments))
        db.commit()

    @staticmethod
    def deassign_roles(user_ids: list[int], roles: list[RoleEnum], db: Session):
        if not user_ids or not roles:
            return

        db_roles = db.query(Role).filter(Role.role.in_(roles)).all()
        role_ids = [r.id for r in db_roles]

        if role_ids:
            db.query(RoleAssignment).filter(
                RoleAssignment.user_id.in_(user_ids),
                RoleAssignment.role_id.in_(role_ids),
            ).update({RoleAssignment.is_assigned: False}, synchronize_session=False)

            db.commit()

    @staticmethod
    def sync_users_to_project(project_id: int, user_ids: list[int], db: Session):
        db.query(ProjectAssignment).filter(
            ProjectAssignment.project_id == project_id,
            ProjectAssignment.user_id.notin_(user_ids),
        ).update({ProjectAssignment.is_assigned: False}, synchronize_session=False)

        if not user_ids:
            db.commit()
            return

        db.query(ProjectAssignment).filter(
            ProjectAssignment.project_id == project_id,
            ProjectAssignment.user_id.in_(user_ids),
        ).update({ProjectAssignment.is_assigned: True}, synchronize_session=False)

        existing_user_ids = set(
            row.user_id for row in db.query(ProjectAssignment.user_id).filter(
                ProjectAssignment.project_id == project_id,
                ProjectAssignment.user_id.in_(user_ids),
            ).all()
        )
        new_assignments = [
            {"user_id": u_id, "project_id": project_id, "is_assigned": True}
            for u_id in user_ids
            if u_id not in existing_user_ids
        ]
        if new_assignments:
            db.execute(insert(ProjectAssignment).values(new_assignments))
        db.commit()

    @staticmethod
    def sync_projects_to_user(user_id: int, project_ids: list[int], db: Session):
        # Deassign projects not in the list
        db.query(ProjectAssignment).filter(
            ProjectAssignment.user_id == user_id,
            ProjectAssignment.project_id.notin_(project_ids),
        ).update({ProjectAssignment.is_assigned: False}, synchronize_session=False)

        if not project_ids:
            db.commit()
            return

        # Re-assign existing records
        db.query(ProjectAssignment).filter(
            ProjectAssignment.user_id == user_id,
            ProjectAssignment.project_id.in_(project_ids),
        ).update({ProjectAssignment.is_assigned: True}, synchronize_session=False)

        # Insert missing records
        existing_project_ids = set(
            row.project_id for row in db.query(ProjectAssignment.project_id).filter(
                ProjectAssignment.user_id == user_id,
                ProjectAssignment.project_id.in_(project_ids),
            ).all()
        )
        new_assignments = [
            {"user_id": user_id, "project_id": p_id, "is_assigned": True}
            for p_id in project_ids
            if p_id not in existing_project_ids
        ]
        if new_assignments:
            db.execute(insert(ProjectAssignment).values(new_assignments))
        db.commit()

    @staticmethod
    def sync_roles_to_user(user_id: int, roles: list[RoleEnum], db: Session):
        db_roles = db.query(Role).filter(Role.role.in_(roles)).all()
        role_ids = [r.id for r in db_roles]

        # Deassign roles not in the list
        query = db.query(RoleAssignment).filter(RoleAssignment.user_id == user_id)
        if role_ids:
            query = query.filter(RoleAssignment.role_id.notin_(role_ids))
        query.update({RoleAssignment.is_assigned: False}, synchronize_session=False)

        if not role_ids:
            db.commit()
            return

        db.query(RoleAssignment).filter(
            RoleAssignment.user_id == user_id,
            RoleAssignment.role_id.in_(role_ids),
        ).update({RoleAssignment.is_assigned: True}, synchronize_session=False)

        existing_role_ids = set(
            row.role_id for row in db.query(RoleAssignment.role_id).filter(
                RoleAssignment.user_id == user_id,
                RoleAssignment.role_id.in_(role_ids),
            ).all()
        )
        new_assignments = [
            {"user_id": user_id, "role_id": r_id, "is_assigned": True}
            for r_id in role_ids
            if r_id not in existing_role_ids
        ]
        if new_assignments:
            db.execute(insert(RoleAssignment).values(new_assignments))
        db.commit()

