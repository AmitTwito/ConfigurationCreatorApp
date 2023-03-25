from datetime import datetime
from enum import Enum


class LogType(Enum):
    MESSAGE = 0
    ERROR = 1


class Log:
    def __init__(self, text: str, log_type: LogType):
        self._text = text
        self._log_type = log_type

    @property
    def text(self):
        return self._text

    @property
    def type(self):
        return self._log_type


class Logger:
    def __init__(self):
        self._logs = [Log("Configuration Creator V1", LogType.MESSAGE),
                      Log("Please make sure to insert correct inputs.", LogType.MESSAGE)]

    def add_log(self, text: str, log_type: LogType):
        text = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {text}'
        self._logs.append(Log(text, log_type))

    @property
    def logs(self):
        return self._logs
