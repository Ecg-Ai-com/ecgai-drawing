from enum import IntEnum


class ColorStyle(IntEnum):
    black_and_white = 1  # 'black_and_white'
    color = 2  # 'color'
    mask = 3  # 'mask'
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
