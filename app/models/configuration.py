import yaml
import json
import os
import os.path
from enum import Enum

from app.models.user import User, UserType

DEFAULT_CONFIG_PATH = "config.yaml"


class Mode(Enum):
    DEBUG = 0
    PRODUCTION = 1


class Configuration:

    def __init__(self, file_path=DEFAULT_CONFIG_PATH):
        self.mode = Mode.DEBUG
        self.tests = [1, 2, 3]
        self.users = [User(user_type=UserType.ADMIN, email="admin@gmail.com", password="admin123456"),
                      User(user_type=UserType.STANDARD, email="employee@gmail.com", password="User123456")]
        self.chosen_image_path = ""
        self.is_use_hardware_acceleration = False
        self.config_file_name = file_path

    def read_from_file(self):
        with open(self.config_file_name, "r") as file:
            data = yaml.safe_load(file)

    def save_to_file(self):
        json_string = '{}'
        json_dict = json.loads(json_string)
        yaml_object = yaml.dump(json_dict)
        with open(self.config_file_name, "w") as stream:
            try:
                print(stream.write(yaml_object))
            except yaml.YAMLError as exc:
                print(exc)
