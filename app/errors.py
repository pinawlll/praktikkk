"""Application errors that map to HTTP responses."""


class ApiError(Exception):
    """Base class for expected errors raised by the service layer."""

    status_code = 400

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ValidationError(ApiError):
    """Invalid input or a business rule violation."""

    status_code = 400


class NotFoundError(ApiError):
    """A requested resource does not exist."""

    status_code = 404
