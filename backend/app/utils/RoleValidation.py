from fastapi import HTTPException, status


class RoleValidation:

    @staticmethod
    def validate_role(current_user: dict, roles: list):
        if not set(current_user["user_roles"]).intersection(set(roles)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )