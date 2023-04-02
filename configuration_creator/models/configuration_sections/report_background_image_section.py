from configuration_creator.enums.configuration_section_enum import ConfigurationSections
from configuration_creator.models.configuration_sections.configuration_section import ConfigurationSection
from configuration_creator.utils.input_validator import InputValidator
from configuration_creator.utils.errors.value_validation_error import ValueValidationError


class ReportBackgroundImageSection(ConfigurationSection):

    def __init__(self, configuration_section_type: ConfigurationSections, template_file: str, ):
        super().__init__(configuration_section_type, template_file)
        self._report_background_image_path = ""
        self._form_keys = [{"key": "image-path", "is_collection": False}]

    def validate(self, path: str):
        if not InputValidator.is_file_path_valid_image(path):
            raise ValueValidationError(
                f"Error at updating the image path. The image path '{path}' is not a valid image, or does not "
                f"exist. Please insert a valid existing image path")
        return path

    def validate_from_yaml(self, path: str):
        if not InputValidator.is_file_path_valid_image(path):
            return {"error": f"Error at reading the image path from the config file. The image path '{path}' is not a "
                             f"valid image, or does not exist. Please insert a valid existing image path"}
        return path

    def update(self, path: str):
        self._report_background_image_path = path

    def as_dict(self) -> dict:
        return {'report_background_image': self._report_background_image_path}
