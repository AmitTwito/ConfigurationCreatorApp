import yaml
import json
from enum import Enum


class Mode(Enum):
    DEBUG = 0
    PRODUCTION = 1


class Configuration:

    def __init__(self):
        self.is_production_mode = False
        self.all_tests = list(range(1, 11))
        self.chosen_tests = [3, 5, 7]
        self.mode_options = [{"value": m.value, "name": m.name, } for m in Mode]
        self.users = []
        self.chosen_image_path = ""
        self.is_use_hardware_acceleration = True
        self.config_file_name = "config.yaml"

    def _read_from_file(self):

        with open(self.config_file_name, "r") as stream:
            try:
                print(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                print(exc)

    def save_to_file(self):
        json_string = '{}'
        dict = json.loads(json_string)
        ymal = yaml.dump(dict)
        with open(self.config_file_name, "w") as stream:
            try:
                print(stream.write(ymal))
            except yaml.YAMLError as exc:
                print(exc)
