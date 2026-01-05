class APIError(Exception):
    status_code: int
    error: str

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ConflictError(APIError):
    status_code = 409
    error = "Conflict"


class NotFoundError(APIError):
    status_code = 404
    error = "Not Found"


class BadRequestError(APIError):
    status_code = 400
    error = "Bad Request"
