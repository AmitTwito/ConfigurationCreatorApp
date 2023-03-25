import yaml
import json
import os
import os.path
from enum import Enum

from app.models.input_validator import InputValidator
from app.models.user import User, UserType

DEFAULT_CONFIG_PATH = "config.yaml"


class Mode(Enum):
    DEBUG = 0
    PRODUCTION = 1


class Configuration:

    def __init__(self, file_path=DEFAULT_CONFIG_PATH):
        self._mode = Mode.DEBUG
        self._tests = [1, 2, 3]
        self.users = [User(user_type=UserType.ADMIN, email="admin@gmail.com", password="admin123456"),
                      User(user_type=UserType.STANDARD, email="employee@gmail.com", password="User123456")]
        self._report_background_image = ""
        self.is_use_hardware_acceleration = False
        self.config_file_name = file_path

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value: Mode):
        self._mode = value

    @property
    def tests(self):
        return self._tests

    @tests.setter
    def tests(self, value: list):
        self._tests = value

    @property
    def report_background_image(self):
        return self._report_background_image

    @report_background_image.setter
    def report_background_image(self, value: str):
        if not InputValidator.is_file_path_valid_image(value):
            raise FileNotFoundError(
                f"Error at updating the image path. The image path '{value}' is not a valid image, or does not exist. "
                f"Please insert a valid image path")
        self._report_background_image = value

    def add_user(self, user_type: UserType, email: str, password: str):
        error_prefix = "Error at adding a new user."
        if not InputValidator.is_email_valid(email) and not InputValidator.is_password_valid(password):
            raise ValueError(
                f"{error_prefix}. The email '{email}' has a wrong format, and the password is empty. Please insert valid values.")

        elif not InputValidator.is_email_valid(email):
            raise ValueError(
                f"{error_prefix}. The password inserted is empty, please insert a valid password")
        elif not InputValidator.is_password_valid(password):
            raise ValueError(
                f"{error_prefix}. The email '{email}' has a wrong format, Please insert valid email address.")

        self.users.append(User(user_type, email, password))

    def delete_user(self, user_id):
        user_id = int(user_id) - 1
        del self.users[user_id]

    def as_dict(self):

        users = [{'type': user.type.name.title(), 'email': user.email, 'password': user.password} for user in
                 self.users]
        return {'mode': self._mode.name.title(), 'tests': self._tests, 'users': users,
                'report-background-image': self.report_background_image,
                'use-hardware-acceleration': self.is_use_hardware_acceleration}

    def read_from_file(self):
        with open(self.config_file_name, "r") as file:
            data = yaml.safe_load(file)

    def save_to_file(self):
        json_string = json.dumps(self.as_dict())
        py_dict = json.loads(json_string)
        yaml_object = yaml.dump(py_dict)
        with open(self.config_file_name, "w") as stream:
            try:
                print(stream.write(yaml_object))
            except yaml.YAMLError as exc:
                print(exc)
