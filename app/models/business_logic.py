import random

import yaml

from app.models.configuration import Configuration, Modes, DEFAULT_CONFIG_PATH
from app.enums.configuration_section_enum import ConfigurationSections
from app.models.logger import Logger, LogTypes
from app.models.user import UserTypes

MAX_RANDOM_SECTIONS_NUMBER = 5
DEFAULT_RANDOM_SECTIONS_NUMBER = 3
DEFAULT_TESTS_NUMBER = 10


class BusinessLogic:
    def __init__(self, config_file_path=DEFAULT_CONFIG_PATH, max_tests_number=DEFAULT_TESTS_NUMBER,
                 number_of_sections_to_randomize=DEFAULT_RANDOM_SECTIONS_NUMBER):
        self._configuration = Configuration(config_file_path)
        self.config_section_to_function = {ConfigurationSections.MODE: self._update_mode,
                                           ConfigurationSections.TESTS: self._update_chosen_tests,
                                           ConfigurationSections.REPORT_BACKGROUND_IMAGE: self._update_report_background_image_path,
                                           ConfigurationSections.HARDWARE_ACCELERATION: self._update_is_use_hardware_acceleration,
                                           ConfigurationSections.USERS: lambda *args: None}
        self.config_section_to_template = {ConfigurationSections.MODE: "mode.html",
                                           ConfigurationSections.TESTS: "tests.html",
                                           ConfigurationSections.USERS: "users_table.html",
                                           ConfigurationSections.REPORT_BACKGROUND_IMAGE: "report_background_image.html",
                                           ConfigurationSections.HARDWARE_ACCELERATION: "hardware_acceleration.html",
                                           }
        self.log_type_colors = {LogTypes.MESSAGE: "black", LogTypes.ERROR: "red"}
        self.config_options = {"modes": Modes, "user_types": UserTypes,
                               "all_tests": list(range(1, max_tests_number + 1)), }
        self.sections_number = number_of_sections_to_randomize

        self._random_sections, self._rest_of_the_sections = [], []
        self._logger = Logger()
        self._start_logging_and_load_config(max_tests_number, number_of_sections_to_randomize)
        self._generate_random_sections_to_display()

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

    def add_log(self, text: str, log_type: LogTypes):
        self._logger.add_log(text, log_type)

    def _start_logging_and_load_config(self, max_tests_number, number_of_sections_to_randomize):
        self._logger.add_log("Script started running", LogTypes.MESSAGE)
        self._logger.add_log("Trying to read config file...", LogTypes.MESSAGE)
        error_prefix = "Problem at reading the config file"
        error_suffix = "Setting configuration to default"
        try:
            self._configuration.read_from_file(max_tests_number)
            self._logger.add_log("Successfully read config file.", LogTypes.MESSAGE)
        except FileNotFoundError as e:
            m = f"{error_prefix}: No valid config.yaml file exists. {error_suffix}"
            self._logger.add_log(m, LogTypes.ERROR)
            self._logger.add_log(str(e), LogTypes.ERROR)
        except ValueError as e:
            m = f"{error_prefix}: Wrong value Error:{e} {error_suffix}"
            self._logger.add_log(m, LogTypes.ERROR)
            self._logger.add_log(str(e), LogTypes.ERROR)
        except Exception as e:
            m = f"{error_prefix}: {e}. {error_suffix}"
            self._logger.add_log(m, LogTypes.ERROR)
            self._logger.add_log(str(e), LogTypes.ERROR)
        self._logger.add_log(
            f"Number of random configuration sections to generate is set to {number_of_sections_to_randomize}",
            LogTypes.MESSAGE)

    def _generate_random_sections_to_display(self, ):
        self._logger.add_log("Generating random configuration sections...", LogTypes.MESSAGE)
        if self.sections_number > MAX_RANDOM_SECTIONS_NUMBER:
            self._logger.add_log("Number of sections to randomly present needs to be 5 or less.", LogTypes.ERROR)
            self._logger.add_log(
                f"The number is set to {DEFAULT_RANDOM_SECTIONS_NUMBER} as default", LogTypes.MESSAGE)
            self._logger.add_log(
                "Please make sure to use valid number.", LogTypes.MESSAGE)
            self.sections_number = DEFAULT_RANDOM_SECTIONS_NUMBER

        self._random_sections = random.sample([section for section in ConfigurationSections], self.sections_number)
        self._random_sections.sort(key=lambda section: section.value)
        self._rest_of_the_sections = list(set(self.config_section_to_template.keys()) - set(self._random_sections))
        self._logger.add_log(f"Finished generating {self.sections_number} random configuration sections.",
                             LogTypes.MESSAGE)

    def _update_mode(self, form):
        mode = form.get('mode-options')
        mode = Modes(int(mode))
        self._configuration.mode = mode

    def _update_chosen_tests(self, form):
        if 'selected-tests' not in form:
            self._configuration.tests = []
        else:
            chosen_tests = form.getlist('selected-tests')
            chosen_tests = [int(test) for test in chosen_tests]
            self._configuration.tests = chosen_tests

    def _update_is_use_hardware_acceleration(self, form):
        self._configuration.is_use_hardware_acceleration = True if form.get('toggle') == 'on' else False

    def _update_report_background_image_path(self, form):
        self._configuration.report_background_image = form.get('image-path')

    def add_user(self, user_type, email: str, password: str):
        try:
            user_type = UserTypes(int(user_type) - 1)
            self._configuration.add_user(user_type, email, password)
        except ValueError as e:
            self._logger.add_log(str(e), LogTypes.ERROR)

        return self._get_page_for_redirection(ConfigurationSections.USERS)

    def delete_user(self, user_id):
        try:
            self._configuration.delete_user(user_id)
        except Exception as e:
            self._logger.add_log(f"Error deleting user with id {user_id}: {e}", LogTypes.ERROR)

        return self._get_page_for_redirection(ConfigurationSections.USERS)

    def save_config_to_file(self):
        try:
            self._logger.add_log("Saving configuration to file...", LogTypes.MESSAGE)
            self._configuration.save_to_file()
            self._logger.add_log("Successfully saved configuration", LogTypes.MESSAGE)
        except yaml.YAMLError as e:
            raise Exception(f'Yaml Error while saving the configuration to file: {str(e)}')
        except Exception as e:
            raise Exception(f'Error saving the configuration to file: {str(e)}')

    def _get_page_for_redirection(self, configuration_section: ConfigurationSections):
        if configuration_section in self.random_sections:
            return '/'
        return '/last_configurations'

    def get_state(self):
        return {"title": "Configuration Creator", "random_sections": self.random_sections,
                "rest_of_the_sections": self._rest_of_the_sections,
                "config_section_to_template": self.config_section_to_template, "users": self._configuration.users,
                "is_use_hardware_acceleration": self._configuration.is_use_hardware_acceleration,
                "config_options": self.config_options, "current_mode": self._configuration.mode,
                "chosen_image_path": self._configuration.report_background_image,
                "tests": self._configuration.tests,
                "logs": self._logger.logs, "log_type_colors": self.log_type_colors}

    def update_config(self, is_randomized_sections, request_form):
        sections = self.random_sections if is_randomized_sections else self._rest_of_the_sections
        for config_section in sections:
            config_section_update_function = self.config_section_to_function[config_section]
            config_section_update_function(request_form)
