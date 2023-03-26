import yaml
import json

from app.enums.configuration_section_enum import ConfigurationSections
from app.utils.config_file_validator import ConfigFileValidator
from app.enums.mode_enum import Modes
from app.utils.input_validator import InputValidator
from app.models.user import User, UserTypes

DEFAULT_CONFIG_PATH = "config.yaml"


class Configuration:

    def __init__(self, file_path=DEFAULT_CONFIG_PATH):
        self._mode = Modes.DEBUG
        self._tests = []
        self.users = [User(user_type=UserTypes.ADMIN, email="admin@gmail.com", password="admin123456"), ]
        self._report_background_image_path = ""
        self._is_use_hardware_acceleration = False
        self.config_file_path = file_path

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value: Modes):
        self._mode = value

    @property
    def tests(self):
        return self._tests

    @tests.setter
    def tests(self, value: list):
        self._tests = value

    @property
    def report_background_image(self):
        return self._report_background_image_path

    @property
    def is_use_hardware_acceleration(self):
        return self._is_use_hardware_acceleration

    @is_use_hardware_acceleration.setter
    def is_use_hardware_acceleration(self, value: bool):
        self._is_use_hardware_acceleration = value

    @report_background_image.setter
    def report_background_image(self, value: str):
        if not InputValidator.is_file_path_valid_image(value):
            raise FileNotFoundError(
                f"Error at updating the image path. The image path '{value}' is not a valid image, or does not exist. "
                f"Please insert a valid existing image path")
        self._report_background_image_path = value

    def add_user(self, user_type: UserTypes, email: str, password: str):
        error_prefix = "Error at adding a new user."
        if not InputValidator.is_email_valid(email) and not InputValidator.is_password_valid(password):
            raise ValueError(
                f"{error_prefix}. The email '{email}' has a wrong format, and the password is empty. Please insert "
                f"valid values.")
        elif not InputValidator.is_email_valid(email):
            raise ValueError(
                f"{error_prefix}. The password inserted is empty, please insert a valid password")
        elif not InputValidator.is_password_valid(password):
            raise ValueError(
                f"{error_prefix}. The email '{email}' has a wrong format, Please insert valid email address.")

        self.users.append(User(user_type, email, password))

    def delete_user(self, user_id):
        user_id = int(user_id) - 1
        if user_id < 0 or user_id >= len(self.users):
            raise IndexError(f"Error in deleting user with id {user_id} as it does not exist.")
        del self.users[user_id]

    def as_dict(self):

        users = [{'type': user.type.name, 'email': user.email, 'password': user.password} for user in
                 self.users]
        return {'mode': self._mode.name, 'tests': self._tests, 'users': users,
                'report_background_image': self._report_background_image_path,
                'hardware_acceleration': self._is_use_hardware_acceleration}

    def as_dict_for_yaml(self):
        config_dict = self.as_dict()
        config_dict[ConfigurationSections.REPORT_BACKGROUND_IMAGE.yaml_key_name] = config_dict.pop(
            'report_background_image')
        config_dict[ConfigurationSections.HARDWARE_ACCELERATION.yaml_key_name] = config_dict.pop(
            'hardware_acceleration')
        return config_dict

    def read_from_file(self, max_tests_number):
        with open(self.config_file_path, "r") as file:
            yaml_object = yaml.safe_load(file)
            ConfigFileValidator.validate_config_yaml_file(self.config_file_path, yaml_object, max_tests_number)
            self.from_yaml_object(yaml_object)

    def save_to_file(self):
        yaml_object = yaml.dump(self.as_dict_for_yaml())
        with open(self.config_file_path, "w") as file:
            file.write(yaml_object)

    def from_yaml_object(self, yaml_object):
        self._mode = Modes.get_by_name(yaml_object[ConfigurationSections.MODE.yaml_key_name])
        self._is_use_hardware_acceleration = yaml_object[ConfigurationSections.HARDWARE_ACCELERATION.yaml_key_name]
        self._report_background_image_path = yaml_object[ConfigurationSections.REPORT_BACKGROUND_IMAGE.yaml_key_name]
        self._tests = yaml_object[ConfigurationSections.TESTS.yaml_key_name]
        users = yaml_object[ConfigurationSections.USERS.yaml_key_name]
        self._users = [User(UserTypes.get_by_name(user['type']),user['email'],user['password']) for user in users]
