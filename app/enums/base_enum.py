from enum import Enum
from types import DynamicClassAttribute


class BaseEnum(Enum):

    @DynamicClassAttribute
    def name(self):
        return super(BaseEnum,self).name.title()

    @property
    def yaml_key_name(self):
        return super(BaseEnum,self).name.lower().replace('_', '-')
