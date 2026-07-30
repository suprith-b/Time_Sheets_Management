from app.core.exceptions import AccessDeniedError


class RoleValidation:

    @staticmethod
    def validate_role(current_user: dict, roles: list):
        if not set(current_user["user_roles"]).intersection(set(roles)):
            raise AccessDeniedError()
