import os
import re
import filetype


class InputValidator:

    @classmethod
    def is_email_valid(cls, email):
        #  https://www.tutorialspoint.com/python-program-to-validate-email-address
        match = re.match(
            r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$", email)
        return bool(match)

    @classmethod
    def is_file_path_valid_image(cls, path: str):
        return InputValidator.is_file_path_exists(path) and InputValidator.is_file_path_image(path)

    @classmethod
    def is_password_valid(cls, password):
        return password

    @classmethod
    def is_file_path_exists(cls, path: str):
        return path is not None and isinstance(path, str) and os.path.exists(path)

    @classmethod
    def is_file_path_image(cls, path: str):
        return filetype.is_image(path)

    @classmethod
    def is_file_mimetype_image(cls, mimetype: str):
        return mimetype.startswith("image")
