class AppException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, message: str = "Ресурс не знайдено"):
        super().__init__(404, message)


class DatabaseException(AppException):
    def __init__(self, message: str = "Помилка бази даних"):
        super().__init__(500, message)


class ValidationException(AppException):
    def __init__(self, message: str = "Некоректні дані"):
        super().__init__(400, message)


class PermissionException(AppException):
    def __init__(self, message: str = "Недостатньо прав"):
        super().__init__(403, message)