import pathlib

from configuration_creator.enums.configuration_section_enum import ConfigurationSections
from configuration_creator.models.configuration_sections.configuration_section import ConfigurationSection
from configuration_creator.utils.input_validator import InputValidator
from configuration_creator.utils.errors.value_validation_error import ValueValidationError
import os

from defaults import DEFAULT_UPLOADS_DIR


class ReportBackgroundImageSection(ConfigurationSection):

    def __init__(self, configuration_section_type: ConfigurationSections, template_file: str, ):
        super().__init__(configuration_section_type, template_file)
        self._report_background_image_path = ""
        self._form_keys = [{"key": "report-background-image-path", "is_collection": False}]
        self._file_keys = [{"key": "report-background-image", "is_collection": False}]
        self._is_file_uploaded = False

    def validate(self, path: str):
        if self._is_file_uploaded:
            return self._report_background_image_path
        if not InputValidator.is_file_path_valid_image(path):
            raise ValueValidationError(
                f"Error at updating the background image path. The image path '{path}' is not a valid image, "
                f"or does not exist. Please insert a valid existing image path")

        return path

    def validate_from_yaml(self, path: str):
        if not InputValidator.is_file_path_valid_image(path):
            return {
                "error": f"Error at reading the background image path from the config file. The image path '{path}' "
                         f"is not a valid image, or does not exist. Please insert a valid existing image path"}
        return path

    def validate_files_and_update(self, files):
        if not files:
            self._is_file_uploaded = False
            return
        super().validate_files_and_update(files)
        self._is_file_uploaded = True

    def validate_and_update(self, value):

        super().validate_and_update(value)
        self._is_file_uploaded = False

    def validate_files(self, files):

        file = files
        if isinstance(files, list) and len(file) > 0:
            file = files[0]
        file_name = file.filename
        if InputValidator.is_file_mimetype_image(file.mimetype):
            configuration_creator_path = os.path.join(DEFAULT_UPLOADS_DIR, os.path.basename(file_name))
            pathlib.Path(DEFAULT_UPLOADS_DIR).mkdir(parents=True, exist_ok=True)
            file.save(configuration_creator_path)
            self._is_file_uploaded = True
            return configuration_creator_path
        raise ValueValidationError(
            f"Error at updating the background image path. The file chosen from the file browser {file_name} "
            f"is not a valid image, or does not exist. Please insert a valid existing image path")

    def update(self, path: str):
        self._report_background_image_path = path

    def as_dict(self) -> dict:
        return {'report_background_image': self._report_background_image_path}
