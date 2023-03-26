from app.enums.configuration_section_enum import ConfigurationSections
from app.enums.mode_enum import Modes
from app.enums.user_type_enum import UserTypes
from app.utils.input_validator import InputValidator


class ConfigFileValidator:

    @classmethod
    def validate_config_yaml_file(cls, config_file_path: str, yaml_object: dict, max_tests_number: int):
        missing_valid_keys_error_message = f"The config file {config_file_path} is missing the following " \
                                           f"sections:"
        yaml_config_file_keys = [section.yaml_key_name for section in ConfigurationSections]

        missing_keys = []
        for key in yaml_config_file_keys:
            if key not in yaml_object:
                missing_keys.append(key)
        if missing_keys:
            raise KeyError(f"{missing_valid_keys_error_message} {missing_keys}")

        modes = {mode.name: mode for mode in Modes}
        user_types = {user_type.name: user_type for user_type in UserTypes}

        invalid_values_error_message = "The config file {self.config_file_name} have some wrong values:"

        if yaml_object['mode'] not in modes.keys():
            invalid_values_error_message += f"\nWrong mode value. Please choose a valid from:{modes.keys()}"

        tests = yaml_object['tests']
        if len(set(tests)) > max_tests_number:
            invalid_values_error_message += f"\nThe number of tests is greater than the max number of tests which is {max_tests_number - 1}"

        if [test not in range(1, max_tests_number) for test in tests]:
            invalid_values_error_message += f"\nTest numbers need to be within range 1 to {max_tests_number - 1}"

        report_background_image_path = yaml_object['report-background-image']
        if not InputValidator.is_file_path_valid_image(report_background_image_path):
            raise ValueError(
                f"The image path '{report_background_image_path}' is not a valid image, or does not exist..")

