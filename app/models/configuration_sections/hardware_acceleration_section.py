from app.enums.configuration_section_enum import ConfigurationSections
from app.models.configuration_sections.configuration_section import ConfigurationSection


class HardwareAccelerationSection(ConfigurationSection):

    def __init__(self, configuration_section_type: ConfigurationSections, template_file: str):
        super().__init__(configuration_section_type, template_file)
        self._is_use_hardware_acceleration = False

    @property
    def is_hardware_acceleration_toggle_on(self):
        return self._is_use_hardware_acceleration

    @is_hardware_acceleration_toggle_on.setter
    def is_hardware_acceleration_toggle_on(self, value: bool):
        raise AttributeError('Setting the is_toggle_on attr is forbidden')

    def update_from_yaml_object(self, yaml_object):
        super().update_from_yaml_object(yaml_object)

    def validate_and_update(self, form):
        super().validate_and_update(form)

    def validate(self):
        pass

    def update(self, form):
        pass

    def as_dict(self) -> dict:
        return {"hardware_acceleration": self._is_use_hardware_acceleration}
