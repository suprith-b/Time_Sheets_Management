from sqlalchemy.orm import Session, aliased

from app.models.PasswordModel import Password
from app.models.ProjectAssignmentModel import ProjectAssignment
from app.models.RoleAssignmentModel import RoleAssignment
from app.models.RoleModel import Role, RoleEnum
from app.models.UserModel import User

import app.schemas.UserSchema as UserSchema
from app.repositories.ProjectRepository import ProjectRepository
from app.utils.security import hash_password


class UserRepository:

    @staticmethod
    def get_user_by_id( user_id: int, db: Session ):
        user = db.query( User ).filter( User.id == user_id ).first()
        if user is None:
            return None
        roles = UserRepository.get_user_roles( user_id, db )
        return { "user": user, "roles": roles }

    @staticmethod
    def are_users_present(user_ids: list[int], db: Session) -> bool:
        return db.query(User.id).filter(User.id.in_(user_ids)).count() == len(set(user_ids))

    @staticmethod
    def check_user_roles( user_ids: list[ int ], role: RoleEnum, db: Session ) -> bool:
        role_id = db.query( Role ).filter( Role.role == role ).first().id
        return db.query( RoleAssignment ).filter(
            RoleAssignment.user_id.in_( user_ids ),
            RoleAssignment.role_id == role_id,
            RoleAssignment.is_assigned
        ).count() == len( user_ids )

    @staticmethod
    def get_users(
        db: Session,
        roles: list[RoleEnum],
        manager_id: int | None,
        is_alive: list[int],
        project_ids: list[int] | None,
        current_user: dict,
    ):
        ManagerUser = aliased(User)
        query = (
            db.query(
                User.id.label("id"),
                User.userid.label( "userid" ),
                User.name.label("user_name"),
                Password.username.label("username"),
                User.manager_id,
                ManagerUser.name.label("manager_name"),
                Role.role,
                User.is_alive.label("is_alive"),
            )
            .join(RoleAssignment, User.id == RoleAssignment.user_id)
            .join(Role, RoleAssignment.role_id == Role.id)
            .outerjoin(Password, User.id == Password.user_id)
            .outerjoin(ManagerUser, User.manager_id == ManagerUser.id)
            .filter(Role.role.in_(roles))
            .filter(RoleAssignment.is_assigned.is_(True))
            .filter(User.is_alive.in_([bool(x) for x in is_alive]))
        )

        if project_ids:
            query = query.join(ProjectAssignment, User.id == ProjectAssignment.user_id).filter(
                ProjectAssignment.project_id.in_(project_ids),
                ProjectAssignment.is_assigned.is_(True),
            )

        if "admin" not in current_user["user_roles"]:
            query = query.filter(User.manager_id == current_user["user_id"])
        elif manager_id is not None:
            query = query.filter(User.manager_id == manager_id)

        rows = query.all()

        users_map = {}
        for row in rows:
            role_val = row.role.value if hasattr(row.role, "value") else str(row.role)
            if row.id not in users_map:
                users_map[row.id] = {
                    "id": row.id,
                    "name": row.user_name or row.username,
                    "username": row.username,
                    "userid": row.userid,
                    "manager_id": row.manager_id,
                    "manager_name": row.manager_name,
                    "roles": [role_val],
                    "is_alive": row.is_alive,
                }
            elif role_val not in users_map[row.id]["roles"]:
                users_map[row.id]["roles"].append(role_val)
        return list(users_map.values())


    @staticmethod
    def create_user(data: UserSchema.CreateUserRequest, db: Session):
        user = User(
            name=data.name,
            userid=data.userid,
            personal_mail=data.personal_mail,
            company_mail=data.company_mail,
            is_alive=True,
        )

        db.add(user)
        db.flush()

        db.add(
            Password(
                user_id=user.id, 
                username=data.username, 
                password=hash_password(data.password)
            )
        )

        if data.roles is None:
            data.roles = [RoleEnum.EMPLOYEE]
        roles = db.query(Role).filter(Role.role.in_(data.roles)).all()
        for role in roles:
            db.add(RoleAssignment(user_id=user.id, role_id=role.id))

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def edit_user(user_id: int, data: UserSchema.EditUserRequest, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            if key == "is_alive":
                user.is_alive = True if value == 1 else False
            elif hasattr(user, key):
                setattr(user, key, value)

        if data.username:
            pwd_entry = db.query(Password).filter(Password.user_id == user_id).first()
            if pwd_entry:
                pwd_entry.username = data.username

        db.commit()
        db.refresh(user)
        pwd_entry = db.query(Password).filter(Password.user_id == user_id).first()
        return user, pwd_entry.username

    @staticmethod
    def update_password(user_id: int, data: UserSchema.UpdatePasswordRequest, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        pwd_entry = db.query(Password).filter(Password.user_id == user_id).first()
        if pwd_entry:
            pwd_entry.password = hash_password(data.password)

        db.commit()
        return user

    @staticmethod
    def soft_delete_user(user_id: int, db: Session):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        user.is_alive = False
        db.commit()
        return user

    @staticmethod
    def get_user_roles(user_id: int, db: Session) -> list[str]:
        rows = (
            db.query(Role.role)
            .join(RoleAssignment, RoleAssignment.role_id == Role.id)
            .filter(
                RoleAssignment.user_id == user_id,
                RoleAssignment.is_assigned.is_(True),
            )
            .all()
        )
        return [row.role.value for row in rows]

    @staticmethod
    def get_user_detail_by_id(user_id: int, db: Session):
        ManagerUser = aliased(User)
        row = (
            db.query(
                User,
                Password.username,
                ManagerUser.name.label("manager_name"),
            )
            .filter(User.id == user_id)
            .outerjoin(Password, User.id == Password.user_id)
            .outerjoin(ManagerUser, User.manager_id == ManagerUser.id)
            .first()
        )
        if not row:
            return None

        user, username, manager_name = row.User, row.username, row.manager_name
        roles = UserRepository.get_user_roles(user_id, db)
        projects = ProjectRepository.get_user_projects(user_id, db)

        return {
            "id": user.id,
            "userid": user.userid,
            "username": username or "",
            "name": user.name,
            "personal_mail": user.personal_mail,
            "company_mail": user.company_mail,
            "is_alive": user.is_alive,
            "roles": roles,
            "projects": projects,
            "manager_id": user.manager_id,
            "manager_name": manager_name,
        }
