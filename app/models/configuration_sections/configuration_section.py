from app.enums.configuration_section_enum import ConfigurationSections


class ConfigurationSection(object):

    def __init__(self, configuration_section_type: ConfigurationSections, template_file: str):
        self._configuration_section_type = configuration_section_type
        self._template_file = template_file

    @property
    def template_file(self):
        return self._template_file

    @template_file.setter
    def template_File(self, value):
        raise AttributeError('Setting the template_file attr is forbidden')

    @property
    def configuration_section_type(self):
        return self._configuration_section_type

    @configuration_section_type.setter
    def configuration_section_type(self, value):
        raise AttributeError('Setting the template_file attr is forbidden')

    def as_dict(self) -> dict:
        pass

    def as_dict_for_yaml(self) -> dict:
        pass

    def validate_and_update_from_yaml(self, value):
        validated_value = self.validate_from_yaml(value)
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
