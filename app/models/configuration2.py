import yaml

from app.enums.configuration_section_enum import ConfigurationSections
from configuration_sections.mode_section import ModeSection
from configuration_sections.users_section import UsersSection
from configuration_sections.hardware_acceleration_section import HardwareAccelerationSection
from configuration_sections.tests_section import TestsSection
from configuration_sections.report_background_image_section import ReportBackgroundImageSection

DEFAULT_CONFIG_PATH = "config.yaml"


class Configuration:
    def __init__(self, template_files_names, file_path=DEFAULT_CONFIG_PATH, ):
        self._sections = [ModeSection(ConfigurationSections.MODE, template_files_names[ConfigurationSections.MODE]),
                          TestsSection(ConfigurationSections.TESTS, template_files_names[ConfigurationSections.TESTS]),
                          HardwareAccelerationSection(ConfigurationSections.HARDWARE_ACCELERATION,
                                                      template_files_names[
                                                          ConfigurationSections.HARDWARE_ACCELERATION]),
                          ReportBackgroundImageSection(ConfigurationSections.REPORT_BACKGROUND_IMAGE,
                                                       template_files_names[
                                                           ConfigurationSections.REPORT_BACKGROUND_IMAGE]),
                          UsersSection(ConfigurationSections.USERS,
                                       template_files_names[ConfigurationSections.USERS])]

        self._sections.sort(key=lambda section: section.configuration_section_type)
        self._config_file_path = file_path

    @property
    def sections(self):
        return self._sections

    @sections.setter
    def sections(self, value):
        raise AttributeError("Setting the sections attr is forbidden")

    def as_dict(self):
        config_dict = {}
        section_dicts = [section.as_dict() for section in self._sections]
        for section_dict in section_dicts:
            for k, v in section_dict.items():
                config_dict[k].add(v)
        return config_dict

    # def as_dict_for_yaml(self):
    #     config_dict = self.as_dict()
    #     config_dict[ConfigurationSections.REPORT_BACKGROUND_IMAGE.yaml_key_name] = config_dict.pop(
    #         'report_background_image')
    #     config_dict[ConfigurationSections.HARDWARE_ACCELERATION.yaml_key_name] = config_dict.pop(
    #         'hardware_acceleration')
    #     return config_dict

    def validate_and_update(self, form):
        for section in self._sections:
            section.validate_and_update(section.)

    def read_from_file(self, ):
        with open(self._config_file_path, "r") as file:
            yaml_object = yaml.safe_load(file)
            self._check_missing_sections_existence(yaml_object)
            self.from_yaml_object(yaml_object)

    def _check_missing_sections_existence(self, yaml_object):
        missing_valid_keys_error_message = f"The config file {self._config_file_path} is missing the following " \
                                           f"sections:"
        yaml_config_file_keys = [section.yaml_key_name for section in ConfigurationSections]
        missing_keys = []
        for key in yaml_config_file_keys:
            if key not in yaml_object:
                missing_keys.append(key)
        if missing_keys:
            raise KeyError(f"{missing_valid_keys_error_message} {missing_keys}")

    def save_to_file(self):
        yaml_object = yaml.dump(self.as_dict())
        with open(self._config_file_path, "w") as file:
            file.write(yaml_object)

    def from_yaml_object(self, yaml_object):
        for section in self._sections:
            yaml_key = section.configuration_section_type.name_lower_case
            section.validate_and_update_from_yaml(yaml_object[yaml_key])
