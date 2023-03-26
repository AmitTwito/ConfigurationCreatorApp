from app.enums.configuration_section_enum import ConfigurationSections
from app.enums.mode_enum import Modes
from app.models.configuration_sections.configuration_section import ConfigurationSection


class ModeSection(ConfigurationSection):
    def __init__(self, configuration_section_type: ConfigurationSections, template_file: str):
        super().__init__(configuration_section_type, template_file)
        self._mode = Modes.DEBUG

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        raise AttributeError('Setting the mode attr is forbidden')

    def validate_from_yaml(self, value):
        modes = {mode.name: mode for mode in Modes}
        if value not in modes.keys():
            return {"error": f"\nWrong mode value. Please choose a valid from:{modes.keys()}"}

        return Modes.get_by_name(value)

    def update_from_yaml(self, value):
        self._mode = Modes.get_by_name(value)

    def validate(self, value: Modes):
        pass

    def update(self, value: Modes):
        self._mode = value

    def as_dict(self) -> dict:
        return {'mode': self._mode.name}
