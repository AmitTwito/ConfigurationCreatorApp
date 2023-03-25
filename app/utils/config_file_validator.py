from app.enums.configuration_section import ConfigurationSection
from app.enums.mode import Mode
from app.enums.user_type import UserType
from app.utils.input_validator import InputValidator


class ConfigFileValidator:

    @classmethod
    def validate_config_yaml_file(cls, config_file_path: str, yaml_object, max_tests_number: int):
        missing_valid_keys_error_message = f"The config file {config_file_path} is missing the following " \
                                           f"sections:"
        yaml_config_file_keys = [section.yaml_key_name for section in ConfigurationSection]
        modes = {mode.name: mode for mode in Mode}
        user_types = {user_type.name: user_type for user_type in UserType}
        missing_keys = []
        for key in yaml_config_file_keys:
            if key not in yaml_object:
                missing_keys.append(key)
        if missing_keys:
            raise KeyError(f"{missing_valid_keys_error_message} {missing_keys}")

        invalid_values_error_message = "The config file {self.config_file_name} have some wrong values:"

        if yaml_object['mode'] not in modes:
            invalid_values_error_message += f"\nWrong mode value. Please choose a valid from:{modes.keys()}"

        tests = yaml_object['tests']
        if len(set(tests)) > max_tests_number:
            invalid_values_error_message += f"\nThe number of tests is greater than the max number of tests which is {max_tests_number - 1}"
        if [test not in range(1, max_tests_number) for test in tests]:
            invalid_values_error_message += f"\nTest numbers need to be within range 1 to {max_tests_number - 1}"
        if InputValidator.is_file_path_valid_image(yaml_object['report-background-image']):
            raise ValueError(f"Wrong mode value. Please choose a valid from:{modes.keys()}")
        if yaml_object['mode'] not in modes:
            raise ValueError(f"Wrong mode value. Please choose a valid from:{modes.keys()}")
        if yaml_object['mode'] not in modes:
            raise ValueError(f"Wrong mode value. Please choose a valid from:{modes.keys()}")
