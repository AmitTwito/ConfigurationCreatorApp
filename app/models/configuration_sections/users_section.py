from app.enums.configuration_section_enum import ConfigurationSections
from app.enums.user_type_enum import UserTypes
from app.models.configuration_sections.configuration_section import ConfigurationSection
from app.models.user import User
from app.utils.input_validator import InputValidator


class UsersSection(ConfigurationSection):

    def __init__(self, configuration_section_type: ConfigurationSections, template_file: str):
        super().__init__(configuration_section_type, template_file)
        self._users = []
        # self._form_keys = {"key": "", "is_collection": True}

    @property
    def form_keys(self):
        return {}

    def validate_and_update(self, value):
        pass

    def validate(self, users=list):
        pass

    def validate_from_yaml(self, users):
        error = "Error at reading users from the config file the: "
        theres_any_error = False
        if not isinstance(users, list):
            error += "Users need to be a list of users, containing valid 'type', 'email', 'password'"
            theres_any_error = True
        for user in users:
            if any(prop not in user for prop in ['type', 'email', 'password']):
                error += "At least one of the users is missing 'type' or 'email' or 'password' "
                theres_any_error = True
            if 'email' in user:
                email = user['email']
                if not InputValidator.is_email_valid(email):
                    error += f'The email {email} is not valid.'
                    theres_any_error = True
            if 'type' in user:
                user_type = user['type']
                if not UserTypes.get_by_name(user_type):
                    types = [user_type.name for user_type in UserTypes]
                    error += f'The user type {user_type} is not valid. please choose from within {types}'
                    theres_any_error = True
            if 'password' in user:
                password = user['password']
                if not InputValidator.is_password_valid(password):
                    error += f'The password {password} is not valid.'
                    theres_any_error = True

        if theres_any_error:
            return {"error": error}

        return [User(UserTypes.get_by_name(user['type']), user['email'], user['password']) for user in users]

    def update(self, users):
        pass

    def add_user(self, user_type: UserTypes, email: str, password: str):
        error_prefix = "Error at adding a new user"
        if not InputValidator.is_email_valid(email) and not InputValidator.is_password_valid(password):
            raise ValueError(
                f"{error_prefix}. The email '{email}' has a wrong format, and the password is empty. Please insert "
                f"valid values.")
        elif not InputValidator.is_password_valid(password):
            raise ValueError(
                f"{error_prefix}. The password inserted is empty, please insert a valid password")
        elif not InputValidator.is_email_valid(email):
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
