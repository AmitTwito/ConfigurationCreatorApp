from app.enums.user_type_enum import UserTypes


class User(object):
    def __init__(self, user_type=UserTypes.STANDARD, email="", password=""):
        self._type = user_type
        self._email = email
        self._password = password

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value
