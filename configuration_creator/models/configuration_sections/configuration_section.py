from configuration_creator.enums.configuration_section_enum import ConfigurationSections


class ConfigurationSection(object):

    def __init__(self, configuration_section_type: ConfigurationSections, template_file: str):
        self._configuration_section_type = configuration_section_type
        self._template = template_file
        self._form_keys = []
        self._file_keys = []

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        raise AttributeError('Setting the template_file attr is forbidden')

    @property
    def configuration_section_type(self):
        return self._configuration_section_type

    @configuration_section_type.setter
    def configuration_section_type(self, value):
        raise AttributeError('Setting the template_file attr is forbidden')

    @property
    def form_keys(self):
        return self._form_keys

    @form_keys.setter
    def form_keys(self, value):
        raise AttributeError('Setting the form_keys attr is forbidden')

    @property
    def file_keys(self):
        return self._file_keys

    @file_keys.setter
    def file_keys(self, value):
        raise AttributeError('Setting the form_keys attr is forbidden')

    def as_dict(self) -> dict:
        pass

    def as_dict_for_yaml(self) -> dict:
        pass

    def validate_files_and_update(self, files):
        validated_value = self.validate_files(files)
        self.update(validated_value)

    def validate_files(self, files):
        pass

    def validate_and_update_from_yaml(self, value):
        validated_value = self.validate_from_yaml(value)
        if isinstance(validated_value, dict) and "error" in validated_value:
            return validated_value
        self.update(validated_value)

    def validate_from_yaml(self, value):
        pass

    def validate_and_update(self, value):
        validated_value = self.validate(value)
        self.update(validated_value)

    def validate(self, value) -> any:
        pass

    def update(self, value):
        pass

