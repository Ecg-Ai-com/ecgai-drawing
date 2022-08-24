import pydantic

from ecgai_drawing.enums.artifact import Artifact
from ecgai_drawing.enums.color_style import ColorStyle
from ecgai_drawing.models.ecg_leads import Leads
from ecgai_drawing.models.model_base import MyBaseModel


class DrawEcgPlotRequest(MyBaseModel):
    transaction_id: str
    record_name: str
    sample_rate: int
    color_style: ColorStyle
    show_grid: bool
    artifact: Artifact
    ecg_leads: Leads
    file_name: str

    @classmethod
    def create(
        cls,
        transaction_id: str,
        record_name: str,
        sample_rate: int,
        ecg_leads: Leads,
        color_style: ColorStyle,
        show_grid: bool,
        artifact: Artifact,
        file_name: str,
    ):
        try:
            d = dict(
                TransactionId=transaction_id,
                RecordName=record_name,
                SampleRate=sample_rate,
                EcgLeads=ecg_leads,
                ColorStyle=color_style,
                ShowGrid=show_grid,
                Artifact=artifact,
                FileName=file_name,
            )
            return cls.from_dict(d)
        except pydantic.ValidationError as e:
            # logging.error(e)
            raise e
