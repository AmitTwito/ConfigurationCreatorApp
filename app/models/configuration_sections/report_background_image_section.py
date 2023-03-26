from app.enums.configuration_section_enum import ConfigurationSections
from app.models.configuration_sections.configuration_section import ConfigurationSection
from app.utils.input_validator import InputValidator


class ReportBackgroundImageSection(ConfigurationSection):

    def __init__(self, configuration_section_type: ConfigurationSections, template_file: str,
                 ):
        super().__init__(configuration_section_type, template_file)
        self._report_background_image_path = ""

    def validate_from_yaml(self, path: str):
        if not InputValidator.is_file_path_valid_image(path):
            return {"error":
                        f"Error at updating the image path. The image path '{path}' is not a valid image, or does not "
                        f"exist. Please insert a valid existing image path"}
        return path

    def validate(self, path: str):
        if not InputValidator.is_file_path_valid_image(path):
            raise FileNotFoundError(
                f"Error at updating the image path. The image path '{path}' is not a valid image, or does not exist. "
                f"Please insert a valid existing image path")
        return path

    def update(self, path: str):
        self._report_background_image_path = path

    def as_dict(self) -> dict:
        return {'report_background_image': self._report_background_image_path}
