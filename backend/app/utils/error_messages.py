from dataclasses import dataclass


@dataclass
class GeneralErrorMessages:
    INTERNAL_SERVER_ERROR = "Internal server error"
    NOT_FOUND = "Not found"


@dataclass
class AuthErrorMessages:
    INVALID_CREDENTIALS = "Invalid credentials"
    USER_ALREADY_EXISTS = "User already exists"
