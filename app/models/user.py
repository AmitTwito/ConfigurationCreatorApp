from enum import Enum


class UserTypes(Enum):
    ADMIN: 0
    STANDARD: 1


class User:

    def __init__(self, user_type, email, password):
        self.type = user_type
        self.email = email
        self.password = password
