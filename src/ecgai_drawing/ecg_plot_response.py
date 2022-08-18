from pydantic.dataclasses import dataclass

from ecgai_drawing.enums.artifact import Artifact
from ecgai_drawing.enums.color_style import ColorStyle
from ecgai_drawing.models.ecg_leads import Leads


@dataclass
class DrawEcgPlotResponse:
    transaction_id: str
    record_name: str
    sample_rate: int
    color_style: ColorStyle
    show_grid: bool
    artifact: Artifact
    ecg_leads: Leads
    file_name: str

    def __int__(
        self,
        transaction_id: str,
        record_name: str,
        sample_rate: int,
        ecg_leads: Leads,
        color_style: ColorStyle,
        show_grid: bool,
        artifact: Artifact,
        file_name: str,
    ):
        self.transaction_id = transaction_id
        self.record_name = record_name
        self.sample_rate = sample_rate
        self.color_style = color_style
        self.show_grid = show_grid
        self.artifact = artifact
        self.ecg_leads = ecg_leads
        self.file_name = file_name
