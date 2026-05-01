class HandlingError(Exception):
    def __init__(self, *args, status: int = 400):
        super().__init__(*args)
        self.status = status


class TaskAlreadyFinishedError(HandlingError):
    ...


class UndefinedProjectError(HandlingError):
    ...


class UserDoesNotRelatedToProject(HandlingError):
    ...


class UserAlreadyExists(HandlingError):
    ...


class UndefinedUserError(HandlingError):
    ...


class InvalidPasswordError(HandlingError):
    ...


class AuthError(HandlingError):
    ...
