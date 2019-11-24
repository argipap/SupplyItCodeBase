# services/users/project/api/views/errors.py


class OperationsError(Exception):
    def __init__(self, message):
        self.message = message


class InternalServerError(OperationsError):
    pass
