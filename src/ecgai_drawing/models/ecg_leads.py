from typing import List

from ecgai_drawing.models.ecg_lead import Lead
from ecgai_drawing.models.model_base import MyBaseModel


class Leads(MyBaseModel):
    record_name: str
    sample_rate: int
    leads: List[Lead]

    @classmethod
    def create(cls, record_name: str, sample_rate: int, leads: List[Lead]):
        d = dict(RecordName=record_name, SampleRate=sample_rate, Leads=leads)
        return cls.from_dict(d)

    # def to_json(self):
    #
    #     """
    #     Not implemented in this model as issues with EcgLeadNameOld not Json serializable and this model will not be saved
    #     """
    #     raise NotImplementedError()
