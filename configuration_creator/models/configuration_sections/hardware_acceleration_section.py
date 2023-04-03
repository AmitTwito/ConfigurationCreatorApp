from configuration_creator.enums.configuration_section_enum import ConfigurationSections
from configuration_creator.models.configuration_sections.configuration_section import ConfigurationSection
from configuration_creator.utils.errors.value_validation_error import ValueValidationError


class HardwareAccelerationSection(ConfigurationSection):

    def __init__(self, configuration_section_type: ConfigurationSections, template_file: str):
        super().__init__(configuration_section_type, template_file)
        self._is_hardware_acceleration_toggle_on = False
        self._form_keys = [{"key": "toggle-hardware-acceleration", "is_collection": False}]

    @property
    def is_hardware_acceleration_toggle_on(self):
        return self._is_hardware_acceleration_toggle_on

    @is_hardware_acceleration_toggle_on.setter
    def is_hardware_acceleration_toggle_on(self, value: bool):
        raise AttributeError('Setting the is_toggle_on attr is forbidden')

    def validate_from_yaml(self, value):
        if not isinstance(value, bool):
            return {"error": "Error at reading the hardware_acceleration from the config file. "
                             "Wrong hardware_acceleration value. Please use a boolean value"}
        return value

    def validate(self, value):
        if value not in ['on', None]:
            raise ValueValidationError(
                "Error at getting the hardware acceleration toggle value from the request's form. "
                "Wrong toggle value")
        return value == 'on'

    def update(self, is_hardware_acceleration_toggle_on: bool):
        self._is_hardware_acceleration_toggle_on = is_hardware_acceleration_toggle_on

    def as_dict(self) -> dict:
        return {"hardware_acceleration": self._is_hardware_acceleration_toggle_on}
