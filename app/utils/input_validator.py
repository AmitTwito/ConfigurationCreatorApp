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
    def is_file_path_valid_image(cls, path):
        return os.path.exists(path) and filetype.is_image(path)

    @classmethod
    def is_password_valid(cls, password):
        return password != ""
