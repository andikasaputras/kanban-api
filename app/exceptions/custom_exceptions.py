class ClientError(Exception):
    """Raised when the request is bad"""
    def __init__(self, message="Bad request", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(ClientError):
    """Raised when the input is invalid"""
    def __init__(
            self,
            message="The provided input is invalid",
            status_code=400):
        super().__init__(message, status_code)


class UserActionError(ClientError):
    """Raised when there's an error related to user actions"""
    def __init__(
            self,
            message="User action failed",
            status_code=400):
        super().__init__(message, status_code)


class NotFoundError(ClientError):
    """Raised when the user does not exist"""
    def __init__(
            self,
            message="The requested resource does not exist",
            status_code=404):
        super().__init__(message, status_code)


class AlreadyExistsError(ClientError):
    """Raised when the username or email is already taken"""
    def __init__(
            self,
            message="The provided username or email is already in use",
            status_code=409):
        super().__init__(message, status_code)


class PasswordMismatchError(ClientError):
    """Raised when the provided passwords do not match"""
    def __init__(
            self,
            message="The provided passwords do not match",
            status_code=400):
        super().__init__(message, status_code)


class UnauthorizedError(ClientError):
    """Raised when the user is not authorized"""
    def __init__(
            self,
            message="User is not authorized to access this resource",
            status_code=401):
        super().__init__(message, status_code)


class ForbiddenError(ClientError):
    """Raised when the user is forbidden from accessing a resource"""
    def __init__(
            self,
            message="User is forbidden from accessing this resource",
            status_code=403):
        super().__init__(message, status_code)


class InternalServerError(Exception):
    """Raised when the server encounters an internal error"""
    def __init__(self, message="Internal server error", status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DatabaseOperationError(InternalServerError):
    """Raised when there's an error with the database"""
    def __init__(
            self, message="Database operation failed", status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DatabaseValidationError(InternalServerError):
    """Raised when there's an error with the database"""
    def __init__(
            self, message="Database validation failed", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message, self.status_code)
