"""
Custom application exceptions.

The service layer raises these. The router layer catches them
and maps them to the appropriate HTTP status codes.

This keeps HTTP concerns (status codes, response format) entirely
out of the business logic layer.
"""


class AppError(Exception):
    """Base class for all custom application errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(AppError):
    """Raised when a requested resource does not exist in the database."""
    pass


class AlreadyExistsError(AppError):
    """Raised when trying to create a resource that already exists (e.g., duplicate email)."""
    pass


class InvalidCredentialsError(AppError):
    """Raised when login email/password combination is incorrect."""
    pass


class PermissionDeniedError(AppError):
    """Raised when a user tries to perform an action they are not authorized for."""
    pass


class InvalidTokenError(AppError):
    """Raised when a JWT token is missing, expired, or tampered with."""
    pass

