from configuration_creator.enums.configuration_section_enum import ConfigurationSections
from configuration_creator.enums.user_type_enum import UserTypes
from configuration_creator.models.configuration_sections.configuration_section import ConfigurationSection
from configuration_creator.models.user import User
from configuration_creator.utils.input_validator import InputValidator
from configuration_creator.utils.errors.user_creation_error import UserAdditionError
from configuration_creator.utils.errors.user_deletion_error import UserDeletionError
from configuration_creator.utils.errors.value_validation_error import ValueValidationError


def get_emails_and_duplicates_from_users(users):
    emails_list = [user["email"] for user in users]
    emails = set()
    dup_emails = set()
    for email in emails_list:
        dup_emails.add(email) if email in emails else emails.add(email)
    return dup_emails, emails


class UsersSection(ConfigurationSection):

    def __init__(self, configuration_section_type: ConfigurationSections, template_file: str):
        super().__init__(configuration_section_type, template_file)
        self._users = []
        self._emails = set()
        # self._form_keys = {"key": "", "is_collection": True}

    @property
    def form_keys(self):
        return {}

    def validate_and_update(self, value):
        pass

    def validate(self, users=list):
        pass

    def validate_from_yaml(self, users):
        error = "Error at reading users from the config file: "
        theres_any_error = False
        theres_any_error_with_a_user = False
        if not isinstance(users, list):
            error += "\nUsers need to be a list of users, containing valid 'type', 'email', 'password'."
            theres_any_error = True
        for user in users:
            if theres_any_error_with_a_user:
                break
            if not isinstance(user, dict):
                error += "\nEach user needs to be in the format: \n-email: XXXXX\npassword: XXXXX\ntype: XXXXX."
                theres_any_error = True
                theres_any_error_with_a_user = True
            if any(prop not in user for prop in ['type', 'email', 'password']):
                error += "\nAt least one of the users is missing 'type' or 'email' or 'password'. "
                theres_any_error = True
                theres_any_error_with_a_user = True
            if 'email' in user:
                email = user['email']
                if not InputValidator.is_email_valid(email):
                    error += f'\nThe email {email} is not valid.'
                    theres_any_error = True
                    theres_any_error_with_a_user = True
            if 'type' in user:
                user_type = user['type']
                if not UserTypes.get_by_name(user_type):
                    types = [user_type.name for user_type in UserTypes]
                    error += f'\nThe user type {user_type} is not valid. please choose from within {types}'
                    theres_any_error = True
                    theres_any_error_with_a_user = True
            if 'password' in user:
                password = user['password']
                if not InputValidator.is_password_valid(password):
                    error += f'\nThe password {password} is not valid.'
                    theres_any_error = True
                    theres_any_error_with_a_user = True

        dup_emails, emails = get_emails_and_duplicates_from_users(users)
        if dup_emails:
            error += f"\nThere are duplicate emails, each user needs to have a unique email address. " \
                     f"duplicates:{list(dup_emails)} "
            theres_any_error = True

        if theres_any_error:
            return {"error": error}

        return [User(UserTypes.get_by_name(user['type']), user['email'], user['password']) for user in users], emails

    def update(self, users_and_emails):  # need to change implementation?
        self._users, self._emails = users_and_emails[0], users_and_emails[1]

    def add_user(self, user_type: UserTypes, email: str, password: str):
        error_prefix = "Error at adding a new user"
        try:
            error_message = ""
            if not InputValidator.is_email_valid(email) and not InputValidator.is_password_valid(password):
                error_message = f"{error_prefix}. The email '{email}' has a wrong format, and the password is empty. " \
                                f"Please insert valid values."
            elif not InputValidator.is_password_valid(password):
                error_message = f"{error_prefix}. The password inserted is empty, please insert a valid password"
            elif not InputValidator.is_email_valid(email):
                error_message = f"{error_prefix}. The email '{email}' has a wrong format, " \
                                f"Please insert valid email address."
            if email in self._emails:
                error_message = f"{error_prefix}. The email '{email}' already exists, " \
                                f"Please insert a different email address."
            if error_message:
                raise ValueValidationError(error_message)
        except ValueValidationError as e:
            raise UserAdditionError(str(e))

        self._emails.add(email)
        self._users.append(User(user_type, email, password))

    def delete_user(self, user_id):
        try:
            user_id = int(user_id) - 1
            if user_id < 0 or user_id >= len(self._users):
                raise UserDeletionError(f"Error in deleting user with id {user_id} as it does not exist.")
            email = self._users[user_id].email
            self._emails.remove(email)
            del self._users[user_id]
            return email
        except Exception as e:
            raise UserDeletionError(str(e))

    def as_dict(self) -> dict:
        users = [{'type': user.type.name, 'email': user.email, 'password': user.password} for user in
                 self._users]
        return {'users': users}
