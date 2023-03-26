import collections

from app.enums.configuration_section_enum import ConfigurationSections
from app.enums.user_type_enum import UserTypes
from app.models.configuration_sections.configuration_section import ConfigurationSection
from app.models.user import User
from app.utils.input_validator import InputValidator


class UsersSection(ConfigurationSection):

    def __init__(self, configuration_section_type: ConfigurationSections, template_file: str):
        super().__init__(configuration_section_type, template_file)
        self._users = [User(user_type=UserTypes.ADMIN, email="admin@gmail.com", password="admin123456"), ]

    def validate(self, users=list):
        pass

    def validate_from_yaml(self, users):

        return [User(UserTypes.get_by_name(user['type']), user['email'], user['password']) for user in users]

    def update(self, users=list[User]):
        self._users = users

    def add_user(self, user_type: UserTypes, email: str, password: str):
        error_prefix = "Error at adding a new user."
        if not InputValidator.is_email_valid(email) and not InputValidator.is_password_valid(password):
            raise ValueError(
                f"{error_prefix}. The email '{email}' has a wrong format, and the password is empty. Please insert "
                f"valid values.")
        elif not InputValidator.is_email_valid(email):
            raise ValueError(
                f"{error_prefix}. The password inserted is empty, please insert a valid password")
        elif not InputValidator.is_password_valid(password):
            raise ValueError(
                f"{error_prefix}. The email '{email}' has a wrong format, Please insert valid email address.")

        self._users.append(User(user_type, email, password))

    def delete_user(self, user_id):
        user_id = int(user_id) - 1
        if user_id < 0 or user_id >= len(self._users):
            raise IndexError(f"Error in deleting user with id {user_id} as it does not exist.")
        del self._users[user_id]

    def as_dict(self) -> dict:
        users = [{'type': user.type.name, 'email': user.email, 'password': user.password} for user in
                 self._users]
        return {'users': users}
