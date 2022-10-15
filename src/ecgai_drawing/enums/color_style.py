from enum import IntEnum


class ColorStyle(IntEnum):
    BLACK_AND_WHITE = 1  # 'BLACK_AND_WHITE'
    COLOR = 2  # 'COLOR'
    MASK = 3  # 'MASK'
    GREY_SCALE = 4
    # binary = 4  # 'binary'

    # @classmethod
    # def _missing_name_(cls, name):
    #     # noinspection PyTypeChecker
    #     for member in cls:
    #         if member.name.lower() == name.lower():
    #             return member
    #
    # def equals(self, string):
    #     return self.name == string
