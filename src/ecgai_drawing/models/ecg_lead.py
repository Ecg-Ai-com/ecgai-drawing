from typing import List

import pydantic

from ecgai_drawing.enums.ecg_lead_name import LeadName
from ecgai_drawing.models.model_base import MyBaseModel


# @dataclass
class Lead(MyBaseModel):
    lead_name: LeadName  # = Field(..., alias='leadName')v
    signal: List[float]  # = Field(..., alias='signal')

    # noinspection PyMethodParameters
    @pydantic.validator("lead_name", pre=True)
    def lead_name_to_enum(cls, v):
        return LeadName[v]

    @classmethod
    def create(cls, lead_name: str, signal: List[float]):
        try:
            d = dict(LeadName=lead_name, Signal=signal)
            return cls.from_dict(d)
        except pydantic.ValidationError as e:
            # logging.error(e)
            raise e

    def __lt__(self, other):
        return self.lead_name < other.lead_name
