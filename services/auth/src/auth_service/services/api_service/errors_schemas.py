class APIError(Exception):
    status_code: int
    error: str

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class BadRequestError(APIError):
    status_code = 400
    error = "Bad Request"


class UnauthorizedError(APIError):
    status_code = 401
    error = "Unauthorized"


class ForbiddenError(APIError):
    status_code = 403
    error = "Forbidden"


class NotFoundError(APIError):
    status_code = 404
    error = "Not Found"


class ConflictError(APIError):
    status_code = 409
    error = "Conflict"
