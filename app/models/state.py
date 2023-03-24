import datetime
from enum import Enum
import random

from app.models.configuration import Configuration, Mode, DEFAULT_CONFIG_PATH
from app.models.logger import Logger, LogType
from app.models.user import UserType

MAX_RANDOM_SECTIONS_NUMBER = 5
DEFAULT_RANDOM_SECTIONS_NUMBER = 3
DEFAULT_TESTS_NUMBER = 11


class ConfigurationSection(Enum):
    MODE = 1
    TESTS = 2
    USERS = 3
    REPORT_BACKGROUND_IMAGE = 4
    HARDWARE_ACCELERATION = 5


class State:
    def __init__(self, config_file_path=DEFAULT_CONFIG_PATH, max_tests=DEFAULT_TESTS_NUMBER,
                 sections_number=DEFAULT_RANDOM_SECTIONS_NUMBER):
        self.sections_number = sections_number
        self.title = "Configuration Creator"
        self.random_sections, self.rest_of_the_sections = [], []
        self.config = Configuration(config_file_path)
        self.config_options = {"modes": Mode, "user_types": UserType, "all_tests": list(range(1, max_tests)), }
        self.log_type_colors = {LogType.MESSAGE: "black", LogType.ERROR: "red"}
        self.config_section_to_template = {ConfigurationSection.MODE: "mode.html",
                                           ConfigurationSection.TESTS: "tests.html",
                                           ConfigurationSection.USERS: "users_table.html",
                                           ConfigurationSection.REPORT_BACKGROUND_IMAGE: "report_background_image.html",
                                           ConfigurationSection.HARDWARE_ACCELERATION: "hardware_acceleration.html",
                                           }
        self.template_to_function = {"mode.html": self.set_mode, }
        self._logger = Logger()
        self._logger.add_log("Script started running", LogType.MESSAGE)
        self._logger.add_log("Trying to read config file...", LogType.MESSAGE)
        try:
            self.config.read_from_file()
        except:
            m = "No valid config.yaml file exists. Setting configuration to default"
            self._logger.add_log(m, LogType.ERROR)
        self._logger.add_log(f"Number of random configuration sections to generate is set to {sections_number}",
                             LogType.MESSAGE)
        self._generate_random_sections()

    def get_logs(self):
        return self._logger.logs

    def add_log(self, text, log_type):
        self._logger.add_log(text, log_type)

    def _generate_random_sections(self, ):
        self._logger.add_log("Generating random configuration sections...", LogType.MESSAGE)
        if self.sections_number > MAX_RANDOM_SECTIONS_NUMBER:
            self._logger.add_log("Number of sections to randomly present needs to be 5 or less.", LogType.ERROR)
            self._logger.add_log(
                f"The number is set to {DEFAULT_RANDOM_SECTIONS_NUMBER} as default", LogType.MESSAGE)
            self._logger.add_log(
                "Please make sure to use valid number.", LogType.MESSAGE)
            self.sections_number = DEFAULT_RANDOM_SECTIONS_NUMBER
        random_section_numbers = random.sample(range(1, 6), self.sections_number)
        random_section_numbers.sort()
        self.random_sections = [self.config_section_to_template[ConfigurationSection(i)] for i in
                                random_section_numbers]
        self.rest_of_the_sections = list(set(self.config_section_to_template.values()) - set(self.random_sections))
        self._logger.add_log(f"Finished generating {self.sections_number} random configuration sections.",
                             LogType.MESSAGE)

    def set_mode(self, request):
        self.config.mode = Mode()

    def set_chosen_image_path(self, request):
        file = request.form

    def to_dict(self):
        return {"title": self.title, "random_sections": self.random_sections,
                "rest_of_the_sections": self.rest_of_the_sections, "users": self.config.users,
                "is_use_hardware_acceleration": self.config.is_use_hardware_acceleration,
                "config_options": self.config_options, "current_mode": self.config.mode,
                "chosen_image_path": self.config.chosen_image_path,
                "tests": self.config.tests,
                "logs": self.get_logs(), "log_type_colors": self.log_type_colors}

    def change_selected_tests(self):
        self.config.tests = self.config_options["all_tests"]
