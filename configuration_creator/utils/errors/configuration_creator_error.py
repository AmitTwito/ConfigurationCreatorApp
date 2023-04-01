from models.logger import Logger, LogTypes


class ConfigurationCreatorError(Exception):

    def __init__(self, message, errors=None):
        super().__init__(message)
        if errors is None:
            errors = []
        self._errors = [message] + errors

    @property
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, value):
        raise AttributeError("Setting errors is forbidden")
