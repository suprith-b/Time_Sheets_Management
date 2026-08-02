from app.core.exceptions import AccessDeniedError
from app.models.RoleModel import RoleEnum as RE

class RoleValidation:

    @staticmethod
    def validate_role(current_user: dict, roles: list[ RE ]):
        if not set(current_user["user_roles"]).intersection(set(role.value for role in roles)):
            raise AccessDeniedError()
