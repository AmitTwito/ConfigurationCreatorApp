import random

import yaml

# from app.models.configuration import Configuration, Modes, DEFAULT_CONFIG_PATH
from app.enums.mode_enum import Modes
from app.models.configuration import Configuration, DEFAULT_CONFIG_PATH
from app.enums.configuration_section_enum import ConfigurationSections
from app.models.logger import Logger, LogTypes
from app.models.user import UserTypes

DEFAULT_RANDOM_SECTIONS_NUMBER = 3
DEFAULT_TESTS_NUMBER = 10


class BusinessLogic:
    def __init__(self, config_file_path=DEFAULT_CONFIG_PATH, max_tests_number=DEFAULT_TESTS_NUMBER,
                 number_of_sections_to_randomize=DEFAULT_RANDOM_SECTIONS_NUMBER):
        self._config_section_to_template = {ConfigurationSections.MODE: "mode.html",
                                            ConfigurationSections.TESTS: "tests.html",
                                            ConfigurationSections.USERS: "users_table.html",
                                            ConfigurationSections.REPORT_BACKGROUND_IMAGE: "report_background_image.html",
                                            ConfigurationSections.HARDWARE_ACCELERATION: "hardware_acceleration.html",
                                            }
        self._configuration = Configuration(config_section_to_template=self._config_section_to_template,
                                            file_path=config_file_path,
                                            max_tests_number=max_tests_number)

        self.log_type_colors = {LogTypes.MESSAGE: "black", LogTypes.ERROR: "red"}
        self.config_options = {"modes": Modes, "user_types": UserTypes,
                               "all_tests": list(range(1, max_tests_number + 1)), }
        self._number_of_sections_to_randomize = number_of_sections_to_randomize

        self._random_sections, self._rest_of_the_sections = [], []
        self._logger = Logger()
        self._start_logging_and_load_config(number_of_sections_to_randomize)
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

    @random_sections.setter
    def random_sections(self, value):
        raise AttributeError("Setting the random_sections is forbidden")

    @property
    def number_of_sections_to_randomize(self, ):
        return self._number_of_sections_to_randomize

    @number_of_sections_to_randomize.setter
    def number_of_sections_to_randomize(self, value):
        raise AttributeError("Setting the number_of_sections_to_randomize is forbidden")

    def get_logs(self):
        return self._logger.logs

    def add_log(self, text: str, log_type: LogTypes):
        self._logger.add_log(text, log_type)

    def _start_logging_and_load_config(self, number_of_sections_to_randomize):
        self._logger.add_log("Script started running", LogTypes.MESSAGE)
        self._logger.add_log("Trying to read config file...", LogTypes.MESSAGE)
        error_prefix = "Problem at reading the config file"
        error_suffix = "Setting configuration to default"
        try:
            output = self._configuration.read_from_file()
            if output:  # there are errors
                self.add_log("There are few value errors in the config file:", log_type=LogTypes.ERROR)
                for error in output:
                    self.add_log(error["error"], log_type=LogTypes.ERROR)
            else:
                self._logger.add_log("Successfully read config file.", LogTypes.MESSAGE)
        except FileNotFoundError as e:
            m = f"{error_prefix}: No valid config.yaml file exists. {error_suffix}"
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
        if self.number_of_sections_to_randomize > len(ConfigurationSections):
            self._logger.add_log("Number of sections to randomly present needs to be 5 or less.", LogTypes.ERROR)
            self._logger.add_log(
                f"The number is set to {DEFAULT_RANDOM_SECTIONS_NUMBER} as default", LogTypes.MESSAGE)
            self._logger.add_log(
                "Please make sure to use valid number.", LogTypes.MESSAGE)
            self.number_of_sections_to_randomize = DEFAULT_RANDOM_SECTIONS_NUMBER

        self._random_sections = random.sample(self._configuration.sections, self.number_of_sections_to_randomize)
        self._random_sections.sort(key=lambda section: section.configuration_section_type.value)
        self._rest_of_the_sections = list(set(self._configuration.sections) - set(self._random_sections))
        self._logger.add_log(
            f"Finished generating {self.number_of_sections_to_randomize} random configuration sections.",
            LogTypes.MESSAGE)

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
        if configuration_section in [section.configuration_section_type for section in self.random_sections]:
            return '/'
        return '/last_configurations'

    def get_state(self):
        config = self._configuration.as_dict()
        return {"title": "Configuration Creator",
                "random_sections": self.random_sections,
                "rest_of_the_sections": self._rest_of_the_sections,
                "users": config[ConfigurationSections.USERS.name_lower_case],
                "is_hardware_acceleration_toggle_on": config[
                    ConfigurationSections.HARDWARE_ACCELERATION.name_lower_case],
                "current_mode": Modes.get_by_name(config[ConfigurationSections.MODE.name_lower_case]),
                "chosen_image_path": config[ConfigurationSections.REPORT_BACKGROUND_IMAGE.name_lower_case],
                "tests": config[ConfigurationSections.TESTS.name_lower_case],
                "logs": self._logger.logs, "log_type_colors": self.log_type_colors,
                "config_options": self.config_options, "sections_number":len(ConfigurationSections),
                "number_of_sections_to_randomize":self.number_of_sections_to_randomize}

    def validate_and_update_config(self, is_randomized_sections, request_form):
        sections = self.random_sections if is_randomized_sections else self._rest_of_the_sections
        errors = []
        for config_section in sections:
            for form_key in config_section.form_keys:
                key = form_key["key"]
                value = request_form.get(key) if not form_key["is_collection"] else request_form.getlist(key)
                if value is not None:
                    output = config_section.validate_and_update(value)
                    if isinstance(output, dict) and "error" in output:
                        errors.append(output["error"])
        if errors:
            for error in errors:
                self.add_log(error, LogTypes.ERROR)
            raise ValueError("There are few validation errors")
