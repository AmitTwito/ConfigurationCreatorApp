import yaml

from configuration_creator.enums.configuration_section_enum import ConfigurationSections
from configuration_creator.enums.user_type_enum import UserTypes
from configuration_creator.models.configuration_sections.mode_section import ModeSection
from configuration_creator.models.configuration_sections.users_section import UsersSection
from configuration_creator.models.configuration_sections.hardware_acceleration_section import \
    HardwareAccelerationSection
from configuration_creator.models.configuration_sections.tests_section import TestsSection
from configuration_creator.models.configuration_sections.report_background_image_section import \
    ReportBackgroundImageSection
from configuration_creator.defaults import DEFAULT_CONFIG_PATH
from configuration_creator.utils.errors.configuration_creator_error import ConfigurationCreatorError
from configuration_creator.utils.errors.yaml_validation_error import YamlValidationError


class Configuration:
    def __init__(self, max_tests_number: int, config_section_to_template: dict, file_path: str, ):
        self._sections = [
            ModeSection(ConfigurationSections.MODE, config_section_to_template[ConfigurationSections.MODE]),
            TestsSection(ConfigurationSections.TESTS, config_section_to_template[ConfigurationSections.TESTS],
                         max_tests_number),
            HardwareAccelerationSection(ConfigurationSections.HARDWARE_ACCELERATION,
                                        config_section_to_template[
                                            ConfigurationSections.HARDWARE_ACCELERATION]),
            ReportBackgroundImageSection(ConfigurationSections.REPORT_BACKGROUND_IMAGE,
                                         config_section_to_template[
                                             ConfigurationSections.REPORT_BACKGROUND_IMAGE]),
            UsersSection(ConfigurationSections.USERS,
                         config_section_to_template[ConfigurationSections.USERS])]

        self._sections.sort(key=lambda section: section.configuration_section_type.value)
        self._config_file_path = file_path

    @property
    def sections(self):
        return self._sections

    @sections.setter
    def sections(self, value):
        raise AttributeError("Setting the sections attr is forbidden")

    @property
    def config_file_path(self):
        return self._config_file_path

    @config_file_path.setter
    def config_file_path(self, value):
        raise AttributeError("Setting the config_file_path attr is forbidden")

    def as_dict(self):
        config_dict = {}
        section_dicts = [section.as_dict() for section in self._sections]
        for section_dict in section_dicts:
            for k, v in section_dict.items():
                config_dict[k] = v
        return config_dict

    def load_from_file(self, ):
        try:
            with open(self._config_file_path, "r") as file:
                yaml_object = yaml.safe_load(file)
                self._check_missing_sections_existence_from_yaml(yaml_object)
                return self.from_yaml_object(yaml_object)
        except ConfigurationCreatorError as e:
            self._config_file_path = DEFAULT_CONFIG_PATH
            raise ConfigurationCreatorError(f"{e.__class__.__name__}", e.errors)
        except Exception as e:
            self._config_file_path = DEFAULT_CONFIG_PATH
            raise Exception(f"{e.__class__.__name__}: {str(e)}")

    def _check_missing_sections_existence_from_yaml(self, yaml_object):
        missing_valid_keys_error_message = f"The config file {self._config_file_path} is missing the following sections:"
        yaml_config_file_keys = [section.name_lower_case for section in ConfigurationSections]
        missing_keys = []
        for key in yaml_config_file_keys:
            if key not in yaml_object:
                missing_keys.append(key)
        if missing_keys:
            raise YamlValidationError(f"{missing_valid_keys_error_message} {missing_keys}")

    def save_to_file(self):
        yaml_object = yaml.dump(self.as_dict())
        with open(self._config_file_path, "w") as file:
            file.write(yaml_object)

    def from_yaml_object(self, yaml_object):
        errors = []
        for section in self._sections:
            yaml_key = section.configuration_section_type.name_lower_case
            output = section.validate_and_update_from_yaml(yaml_object[yaml_key])
            if isinstance(output, dict) and "error" in output:
                errors.append(output["error"])
        if errors:
            raise YamlValidationError("Config file values validation errors:", errors=errors)

    def add_user(self, user_type: UserTypes, email: str, password: str):
        users_section = self._sections[ConfigurationSections.USERS.value]
        users_section.add_user(user_type, email, password)

    def delete_user(self, user_id):
        users_section = self._sections[ConfigurationSections.USERS.value]
        return users_section.delete_user(user_id)

