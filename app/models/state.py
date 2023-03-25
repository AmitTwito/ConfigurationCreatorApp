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
    MODE = 0
    TESTS = 1
    USERS = 2
    REPORT_BACKGROUND_IMAGE = 3
    HARDWARE_ACCELERATION = 4


class State:
    def __init__(self, config_file_path=DEFAULT_CONFIG_PATH, max_tests=DEFAULT_TESTS_NUMBER,
                 sections_number=DEFAULT_RANDOM_SECTIONS_NUMBER):
        self._configuration = Configuration(config_file_path)
        self.config_section_to_function = {ConfigurationSection.MODE: self._update_mode,
                                           ConfigurationSection.TESTS: self._update_chosen_tests,
                                           ConfigurationSection.REPORT_BACKGROUND_IMAGE: self._update_chosen_image_path,
                                           ConfigurationSection.HARDWARE_ACCELERATION: self._update_is_use_hardware_acceleration,
                                           ConfigurationSection.USERS: lambda *args: None}
        self.config_section_to_template = {ConfigurationSection.MODE: "mode.html",
                                           ConfigurationSection.TESTS: "tests.html",
                                           ConfigurationSection.USERS: "users_table.html",
                                           ConfigurationSection.REPORT_BACKGROUND_IMAGE: "report_background_image.html",
                                           ConfigurationSection.HARDWARE_ACCELERATION: "hardware_acceleration.html",
                                           }
        self.log_type_colors = {LogType.MESSAGE: "black", LogType.ERROR: "red"}
        self.config_options = {"modes": Mode, "user_types": UserType, "all_tests": list(range(1, max_tests)), }
        self.sections_number = sections_number

        self._random_sections, self.rest_of_the_sections = [], []
        self._logger = Logger()
        self._logger.add_log("Script started running", LogType.MESSAGE)
        self._logger.add_log("Trying to read config file...", LogType.MESSAGE)
        try:
            self._configuration.read_from_file()
            self._logger.add_log("Successfully read config file.", LogType.MESSAGE)
        except Exception as e:
            m = "No valid config.yaml file exists. Setting configuration to default"
            self._logger.add_log(m, LogType.ERROR)
        self._logger.add_log(f"Number of random configuration sections to generate is set to {sections_number}",
                             LogType.MESSAGE)
        self._generate_random_sections()

    @property
    def configuration(self):
        raise AttributeError("No access to the config")

    @configuration.setter
    def configuration(self, value):
        raise AttributeError("No access to the config")

    @property
    def random_sections(self, ):
        return self._random_sections

    def get_logs(self):
        return self._logger.logs

    def add_log(self, text: str, log_type: LogType):
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
        random_section_numbers = random.sample(range(0, 5), self.sections_number)
        random_section_numbers.sort()
        self._random_sections = [ConfigurationSection(i) for i in
                                 random_section_numbers]
        self.rest_of_the_sections = list(set(self.config_section_to_template.keys()) - set(self._random_sections))
        self._logger.add_log(f"Finished generating {self.sections_number} random configuration sections.",
                             LogType.MESSAGE)

    def _update_mode(self, form):
        mode = form.get('mode-options')
        mode = Mode(int(mode))
        self._configuration.mode = mode

    def _update_chosen_tests(self, form):

        chosen_tests = form.get('selected-tests')
        chosen_tests = [int(test) for test in chosen_tests]
        self._configuration.tests = chosen_tests

    def _update_is_use_hardware_acceleration(self, form):
        self._configuration.is_use_hardware_acceleration = True if form.get('toggle') == 'on' else False

    def _update_chosen_image_path(self, form):
        self._configuration.report_background_image = form.get('image-path')

    def add_user(self, user_type, email: str, password: str):
        try:
            user_type = UserType(int(user_type) - 1)
            self._configuration.add_user(user_type, email, password)
        except ValueError as e:
            self._logger.add_log(str(e), LogType.ERROR)

        return self._get_page_for_redirection(ConfigurationSection.USERS)

    def delete_user(self, user_id):
        try:
            self._configuration.delete_user(user_id)
        except Exception as e:
            self._logger.add_log(f"Error deleting user with id {user_id}: {e}", LogType.ERROR)

        return self._get_page_for_redirection(ConfigurationSection.USERS)

    def save_config_to_file(self):
        try:
            self._logger.add_log("Saving configuration to file...", LogType.MESSAGE)
            self._configuration.save_to_file()
            self._logger.add_log("Successfully saved configuration", LogType.MESSAGE)
        except Exception as e:
            raise Exception(f'Error saving the configuration to file: {str(e)}')

    def _get_page_for_redirection(self, configuration_section: ConfigurationSection):
        if configuration_section in self.random_sections:
            return '/'
        return '/last_configurations'

    def as_dict(self):
        return {"title": "Configuration Creator", "random_sections": self.random_sections,
                "rest_of_the_sections": self.rest_of_the_sections,
                "config_section_to_template": self.config_section_to_template, "users": self._configuration.users,
                "is_use_hardware_acceleration": self._configuration.is_use_hardware_acceleration,
                "config_options": self.config_options, "current_mode": self._configuration.mode,
                "chosen_image_path": self._configuration.report_background_image,
                "tests": self._configuration.tests,
                "logs": self.get_logs(), "log_type_colors": self.log_type_colors}
