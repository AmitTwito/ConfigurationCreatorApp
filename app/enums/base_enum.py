from enum import Enum
from types import DynamicClassAttribute


class BaseEnum(Enum):

    @DynamicClassAttribute
    def name(self):
        return super(BaseEnum, self).name.title()

    # @property
    # def yaml_key_name(self):
    #     return super(BaseEnum, self).name.lower().replace('_', '-')

    @property
    def name_lower_case(self):
        return super(BaseEnum, self).name.lower()

    @classmethod
    def get_by_name(cls, name):
        name_to_enum_dict = {enum_type.name: enum_type for enum_type in cls}
        if name in name_to_enum_dict.keys():

            return name_to_enum_dict[name]
        return ""
