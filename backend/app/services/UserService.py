from app.utils.InputValidation import InputValidation
from app.core.exceptions import InvalidCredentialsError
from app.repositories.AuthRepository import AuthRepository
from app.repositories.AssignmentRepository import AssignmentRepository
from app.repositories.ProjectRepository import ProjectRepository
from sqlalchemy.orm import Session

from app.core.exceptions import AccessDeniedError, ProjectAssignmentRequiredError, UserNotFoundError
from app.models.RoleModel import RoleEnum as RE
from app.repositories.UserRepository import UserRepository
import app.schemas.UserSchema as UserSchema

from email.message import EmailMessage
import smtplib

from app.core.config import settings



class UserService:

    @staticmethod
    def get_users(
        current_user: dict,
        roles: list[RE],
        manager_id: int | None,
        is_alive: list[int],
        project_ids: list[int] | None,
        has_manager: list[ bool ],
        page: int | None,
        page_size: int | None,
        db: Session,
    ):
        if RE.ADMIN not in current_user.get("user_roles"):
            if manager_id is not None and manager_id != current_user.get("user_id"):
                raise AccessDeniedError()
            else:
                manager_id = current_user.get("user_id")

        if project_ids is not None and RE.ADMIN not in current_user.get("user_roles"):
            if not ProjectRepository.are_projects_assigned( project_ids, current_user.get("user_id"), db):
                raise ProjectAssignmentRequiredError()
        
        if has_manager is None:
            has_manager = [ True, False ]
        
        users_data = UserRepository.get_users(db, roles, manager_id, is_alive, project_ids, has_manager, current_user, page, page_size )
        return [UserSchema.UserResponse(**u) for u in users_data]

    @staticmethod
    def get_user_by_id(user_id: int, current_user: dict, db: Session):
        user_roles = current_user.get("user_roles", [])
        current_user_id = current_user.get("user_id")

        if RE.ADMIN not in user_roles and RE.MANAGER not in user_roles:
            if user_id != current_user_id:
                raise AccessDeniedError()
        
        user_data = UserRepository.get_user_by_id(user_id, db)
        if not user_data:
            raise UserNotFoundError()
        
        if RE.ADMIN in user_roles:
            pass
        elif current_user_id == user_id:
            pass
        elif AssignmentRepository.can_view_users_projects(current_user_id, [ user_id ], db):
            pass
        elif user_data[ "user" ].manager_id is None:
            pass
        else:
            raise AccessDeniedError()

        return UserSchema.UserResponse(**user_data["user"]._mapping, roles=user_data["roles"])



    @staticmethod
    def create_user(data: UserSchema.CreateUserRequest, db: Session):
        data.password = "abc123"
        data.userid = data.userid.lower()

        InputValidation.validate_email( data.company_mail )
        InputValidation.validate_phone_number( data.phone_number )
        InputValidation.validate_length( "user id", data.userid, 10 )
        InputValidation.validate_length( "name", data.name, 80 )
        InputValidation.validate_length( "company email", data.company_mail, 50 )
        InputValidation.validate_length( "username", data.username, 50 )

        

        user = UserRepository.create_user(data, db)
        roles = [r.value for r in data.roles] if data.roles else [RE.EMPLOYEE.value]
        
        return UserSchema.CreateUserResponse(
            id=user.id,
            name=user.name,
            userid=user.userid,
            username=data.username,
            phone_number=user.phone_number,
            company_mail=user.company_mail,
            password = data.password,
            roles=roles,
            manager_id=user.manager_id,
            manager_name=UserRepository.get_user_by_id(user.manager_id, db)['user'].name if user.manager_id else None
        )

    @staticmethod
    def edit_user(user_id: int, data: UserSchema.EditUserRequest, db: Session):
        if data.company_mail:
            InputValidation.validate_email( data.company_mail )
        if data.phone_number:
            InputValidation.validate_phone_number( data.phone_number )
        if data.userid:
            InputValidation.validate_length( "user id", data.userid, 10 )
        if data.name:
            InputValidation.validate_length( "name", data.name, 80 )
        if data.company_mail:
            InputValidation.validate_length( "company email", data.company_mail, 50 )
        if data.username:
            InputValidation.validate_length( "username", data.username, 50 )
            
        result = UserRepository.edit_user(user_id, data, db)
        if result is None:
            raise UserNotFoundError()
        user, username = result
        return UserSchema.UserResponse(
            id=user.id,
            userid = user.userid,
            username=username,
            name = user.name,
            manager_id=user.manager_id,
            manager_name=UserRepository.get_user_by_id(user.manager_id, db)[ 'user' ].name if user.manager_id else None,
            phone_number=user.phone_number,
            roles=UserRepository.get_user_roles(user.id, db),
            company_mail=user.company_mail,
            is_alive=user.is_alive
        )

    @staticmethod
    def update_password(user_id: int, data: UserSchema.UpdatePasswordRequest, db: Session):

        if not UserRepository.get_user_by_id(user_id, db):
            raise UserNotFoundError()

        if not AuthRepository.validate_user_password(user_id, data.old_password, db):
            raise InvalidCredentialsError()
        
        InputValidation.validate_length( "password", data.password, 60 )
        return UserRepository.update_password(user_id, data, db)

    @staticmethod
    def delete_user(user_id: int, db: Session):
        user = UserRepository.soft_delete_user(user_id, db)
        if not user:
            raise UserNotFoundError()
        return {"message": "User soft deleted successfully"}

    @staticmethod
    def send_email(to_email: str, subject: str, body: str):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = settings.GMAIL_ID
        msg["To"] = to_email
        msg.set_content(body)
        msg.add_alternative(body, subtype = "html" )

        APP_PASSWORD = settings.GMAIL_APP_PASSWORD
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(settings.GMAIL_ID, APP_PASSWORD)
                smtp.send_message(msg)
        except Exception as e:
            print( "error:\n\n\n\n\n\n\n\n\n\n", e )
