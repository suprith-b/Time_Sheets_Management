from fastapi import HTTPException, status


class ApplicationHTTPException(HTTPException):
    """Base class for application errors returned to API clients."""


class AccessDeniedError(ApplicationHTTPException):
    def __init__(self, detail: str = "You do not have permission to access this resource"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class RepeatedDataError(ApplicationHTTPException):
    def __init__( self, detail: str = "One or more fields already exist"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class AdminAccessRequiredError(AccessDeniedError):
    def __init__(self):
        super().__init__("You do not have admin access")


class ManagerAccessRequiredError(AccessDeniedError):
    def __init__(self):
        super().__init__("You do not have manager access")


class ProjectAssignmentRequiredError(AccessDeniedError):
    def __init__(self, detail: str = "One or more projects are not assigned to you"):
        super().__init__(detail)


class ManagedUserRequiredError(AccessDeniedError):
    def __init__(self, detail: str = "One or more users do not belong to current manager"):
        super().__init__(detail)


class ArchivedProjectModificationError(AccessDeniedError):
    def __init__(self):
        super().__init__("Managers cannot modify archived projects")


class ProjectFieldUpdateForbiddenError(AccessDeniedError):
    def __init__(self):
        super().__init__("One or more fields cannot be changed by manager")


class ResourceNotFoundError(ApplicationHTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UserNotFoundError(ResourceNotFoundError):
    def __init__(self, detail: str = "User not found"):
        super().__init__(detail)


class ManagerNotFoundError(ResourceNotFoundError):
    def __init__(self):
        super().__init__("Manager not found")


class ProjectNotFoundError(ResourceNotFoundError):
    def __init__(self, detail: str = "Project not found"):
        super().__init__(detail)


class TaskNotFoundError(ResourceNotFoundError):
    def __init__(self):
        super().__init__("Task not found")


class TimeLogNotFoundError(ResourceNotFoundError):
    def __init__(self):
        super().__init__("Time log not found")


class InvalidTimeRangeError(ApplicationHTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="start_time must be less than or equal to end_time")

class InvalidDateRangeError(ApplicationHTTPException):
    def __init__(self, detail: str = "start_date must be less than or equal to end_date"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class InvalidProjectTaskAssignmentError(ApplicationHTTPException):
    def __init__(self, detail: str = "Invalid project_id or task_id"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class InvalidTimeLogSortFieldError(ApplicationHTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="sort_by must be either 'project_name' or 'start_time'")


class AuthenticationError(ApplicationHTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers={"WWW-Authenticate": "Bearer"})


class InvalidCredentialsError(AuthenticationError):
    def __init__(self):
        super().__init__("Invalid credentials")


class AccessTokenMissingError(AuthenticationError):
    def __init__(self):
        super().__init__("Access token not found")


class RefreshTokenMissingError(AuthenticationError):
    def __init__(self):
        super().__init__("Refresh token missing")


class InvalidAuthenticationTokenError(AuthenticationError):
    def __init__(self, detail: str = "Invalid or expired token"):
        super().__init__(detail)
