from datetime import datetime
from enum import Enum
import traceback


class LogTypes(Enum):
    MESSAGE = 0
    ERROR = 1


class Log:
    def __init__(self, text: str, log_type: LogTypes):
        self._text = text
        self._log_type = log_type

    @property
    def text(self):
        return self._text

    @property
    def type(self):
        return self._log_type


class Logger:
    def __init__(self, ):
        self._logs = []

    def _add_log(self, text: str, log_type: LogTypes):
        text = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {text}'
        self._logs.append(Log(text, log_type))

    def add_message(self, message):
        self._add_log(message, LogTypes.MESSAGE)

    def add_error(self, error, ex=None):
        # https://stackoverflow.com/questions/4564559/get-exception-description-and-stack-trace-which-caused-an-exception-all-as-a-st
        if isinstance(ex, Exception):
            print(''.join(traceback.TracebackException.from_exception(ex).format()))
        self._add_log(error, LogTypes.ERROR)

    def add_errors(self, errors, error_suffix="", ex=None):
        if isinstance(ex, Exception):
            print(''.join(traceback.TracebackException.from_exception(ex).format()))
        for error in errors:
            self.add_error(f"{error}", )
        self.add_error(error_suffix, )

    @property
    def logs(self):
        return self._logs
