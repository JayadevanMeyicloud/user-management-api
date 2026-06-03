class UserAlreadyExistsError(Exception):
    status_code = 409
    def __init__(self):
        super().__init__("User already exists")

class InvalidPasswordError(Exception):
    status_code = 400
    def __init__(self):
        super().__init__("Password does not meet requirements")

class InvalidRequestError(Exception):
    status_code = 400
    def __init__(self, message="Invalid request"):
        super().__init__(message)

class InvalidCredentialsError(Exception):
    status_code = 401
    def __init__(self):
        super().__init__("Invalid credentials")