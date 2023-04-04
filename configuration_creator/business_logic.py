import os
import random
from pathlib import Path

from configuration_creator.enums.mode_enum import Modes
from configuration_creator.models.configuration import Configuration
from configuration_creator.enums.configuration_section_enum import ConfigurationSections
from configuration_creator.models.logger import Logger, LogTypes
from configuration_creator.models.user import UserTypes
from .utils.errors.configuration_creator_error import ConfigurationCreatorError
from .utils.errors.value_validation_error import ValueValidationError
from .defaults import DEFAULT_CONFIG_PATH, DEFAULT_RANDOM_SECTIONS_NUMBER, DEFAULT_MAX_TESTS_NUMBER, DEFAULT_UPLOADS_DIR


class BusinessLogic:
    def __init__(self, config_file_path=DEFAULT_CONFIG_PATH, max_tests_number=DEFAULT_MAX_TESTS_NUMBER,
                 number_of_sections_to_randomize=DEFAULT_RANDOM_SECTIONS_NUMBER):
        self._config_section_to_template = {ConfigurationSections.MODE: "mode.html",
                                            ConfigurationSections.TESTS: "tests.html",
                                            ConfigurationSections.USERS: "users_table.html",
                                            ConfigurationSections.REPORT_BACKGROUND_IMAGE: "report_background_image.html",
                                            ConfigurationSections.HARDWARE_ACCELERATION: "hardware_acceleration.html", }
        self._logger = Logger()
        # self._max_tests_number = max_tests_number
        self._max_tests_number, self._number_of_sections_to_randomize = self._validate_and_reset_parameters(
            max_tests_number, number_of_sections_to_randomize)

        self._configuration = Configuration(config_section_to_template=self._config_section_to_template,
                                            file_path=config_file_path,
                                            max_tests_number=self._max_tests_number)

        self.log_type_colors = {LogTypes.MESSAGE: "black", LogTypes.ERROR: "red"}
        self.config_options = {"modes": Modes, "user_types": UserTypes,
                               "all_tests": list(range(1, self._max_tests_number + 1)), }

        self._random_sections, self._rest_of_the_sections = [], []
        self._start_logging_and_load_config(wanted_config_file_path=config_file_path)
        self._generate_random_sections_to_display(number_of_sections_to_randomize)

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

    def add_log(self, text: str, log_type: LogTypes, ex=None):
        self._logger.add_message(text, ) if log_type == LogTypes.MESSAGE else self._logger.add_error(text, ex)

    def _validate_and_reset_parameters(self, max_tests_number: int, number_of_sections_to_randomize: int, ):
        if number_of_sections_to_randomize > len(ConfigurationSections) or number_of_sections_to_randomize <= 0:
            self._logger.add_error("Number of sections to randomly present needs to be between 1 to 5")
            self._logger.add_error(
                f"The number is set to {DEFAULT_RANDOM_SECTIONS_NUMBER} as default")
            self._logger.add_error(
                "Please make sure to use valid number.")
            number_of_sections_to_randomize = DEFAULT_RANDOM_SECTIONS_NUMBER
        else:

            number_of_sections_to_randomize = number_of_sections_to_randomize

        if max_tests_number < 0:
            self._logger.add_error(
                f"Max tests number needs to be positive.setting max tests to {DEFAULT_RANDOM_SECTIONS_NUMBER}")
            max_tests_number = DEFAULT_MAX_TESTS_NUMBER
        else:
            self._logger.add_message(
                f"Max tests number is set to {max_tests_number}", )

        return max_tests_number, number_of_sections_to_randomize

    def _start_logging_and_load_config(self, wanted_config_file_path):
        self._logger.add_message("Script started running")
        self._logger.add_message(
            f"Trying to read config file at {wanted_config_file_path}, the default is {DEFAULT_CONFIG_PATH}", )
        error_prefix = "Problem at reading the config file"
        error_suffix = "Setting configuration to default"
        try:
            self._configuration.load_from_file()
            self._logger.add_message("Successfully read config file.")
        except ConfigurationCreatorError as e:
            self._add_reading_config_file_error_to_log(e.errors, error_suffix=error_suffix, ex=e)
        except FileNotFoundError as e:
            error = f"{error_prefix}: the file {wanted_config_file_path} does not exist or is not a valid yaml file. " \
                    f"\n{error_suffix} "
            self._add_reading_config_file_error_to_log(error, ex=e)
        except Exception as e:
            error = f"{error_prefix}: {str(e)}. {error_suffix}"
            self._add_reading_config_file_error_to_log(error, ex=e)

    def _add_reading_config_file_error_to_log(self, error="", error_suffix="", ex=None):
        self.add_log("There are few errors while reading config file:", log_type=LogTypes.ERROR)
        if isinstance(error, list):
            self._logger.add_errors(errors=error, error_suffix=error_suffix, ex=ex)
        if isinstance(error, str):
            self._logger.add_error(error, )

    def _generate_random_sections_to_display(self, number_of_sections_to_randomize):
        self._logger.add_message(
            f"Number of random configuration sections to generate is set to {number_of_sections_to_randomize}", )
        self._logger.add_message("Generating random configuration sections...", )

        self._random_sections = random.sample(self._configuration.sections, self.number_of_sections_to_randomize)
        if number_of_sections_to_randomize != 5:
            self._random_sections.sort(key=lambda section: section.configuration_section_type.value)
        self._rest_of_the_sections = list(set(self._configuration.sections) - set(self._random_sections))
        self._logger.add_message(
            f"Finished generating {self.number_of_sections_to_randomize} random configuration sections.", )

    def add_user(self, user_type, email: str, password: str):
        try:
            user_type = UserTypes(int(user_type) - 1)
            self._configuration.add_user(user_type, email, password)
            self._logger.add_message(f"User with email {email} was added successfully")
        except Exception as e:
            self._logger.add_error(f"{e.__class__.__name__}: {str(e)}", ex=e)

        return self._get_page_for_redirection(ConfigurationSections.USERS)

    def delete_user(self, user_id):
        try:
            email = self._configuration.delete_user(user_id)
            self._logger.add_message(f"User with email {email} was deleted successfully")

        except Exception as e:
            self._logger.add_error(f"{e.__class__.__name__}: {str(e)}", ex=e)

        return self._get_page_for_redirection(ConfigurationSections.USERS)

    def save_config_to_file(self):
        try:
            self._logger.add_message("Saving configuration to file...", )
            self._configuration.save_to_file()
            self._logger.add_message("Successfully saved configuration", )

        except Exception as e:
            raise Exception(f'{e.__class__.__name__} saving the configuration to file: {str(e)}')

    def get_state(self):
        config = self._configuration.as_dict()
        tests = config[ConfigurationSections.TESTS.name_lower_case]
        return {"title": "Configuration Creator",
                "random_sections": self.random_sections,
                "rest_of_the_sections": self._rest_of_the_sections,
                "users": config[ConfigurationSections.USERS.name_lower_case],
                "is_hardware_acceleration_toggle_on": config[
                    ConfigurationSections.HARDWARE_ACCELERATION.name_lower_case],
                "current_mode": Modes.get_by_name(config[ConfigurationSections.MODE.name_lower_case]),
                "chosen_image_path": config[ConfigurationSections.REPORT_BACKGROUND_IMAGE.name_lower_case],
                "tests": tests, "are_all_tests_selected": len(tests) == self._max_tests_number,
                "logs": self._logger.logs, "log_type_colors": self.log_type_colors,
                "config_options": self.config_options, "sections_number": len(ConfigurationSections),
                "number_of_sections_to_randomize": self.number_of_sections_to_randomize, }

    def validate_and_update_config(self, is_randomized_sections, request_form, request_files=None):
        sections = self.random_sections if is_randomized_sections else self._rest_of_the_sections
        errors = []
        for config_section in sections:
            if request_files:
                for file_key in config_section.file_keys:
                    key = file_key["key"]
                    value = request_files[key] if not file_key["is_collection"] else request_files.getlist(key)
                    try:
                        config_section.validate_files_and_update(value)
                    except ValueValidationError as e:
                        errors.append(str(e))

            for form_key in config_section.form_keys:
                key = form_key["key"]
                value = request_form.get(key) if not form_key["is_collection"] else request_form.getlist(key)
                try:
                    config_section.validate_and_update(value)
                except ValueValidationError as e:
                    errors.append(str(e))

        if errors:
            self._logger.add_errors(errors)
            raise ValueValidationError("There are few validation errors")

    def _get_page_for_redirection(self, configuration_section: ConfigurationSections):
        if configuration_section in [section.configuration_section_type for section in self.random_sections]:
            return '/'
        return '/last_configurations'

    def get_configuration_data(self):
        return self._configuration.as_dict()
