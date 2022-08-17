from ecgai_drawing.enums.enum_ordered_base import OrderedEnum


class LeadName(OrderedEnum):
    I = 1
    II = 2
    III = 3
    aVR = 4
    aVL = 5
    aVF = 6
    V1 = 7
    V2 = 8
    V3 = 9
    V4 = 10
    V5 = 11
    V6 = 12
    Unknown = 13

    @classmethod
    def _missing_name_(cls, name):
        # noinspection PyTypeChecker
        for member in cls:
            if member.name.lower() == name.lower():
                return member
        return cls.Unknown
