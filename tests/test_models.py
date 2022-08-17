from typing import List

import numpy as np
import pytest

# def setup_test_record_data():
#     path = os.path.join(sys.path[0], 'test_data', '00001_hr.json')
#     with open(path) as json_file:
#         data = json.load(json_file)
#     record = Leads.from_json(data)
#     assert type(record) is Leads
#     return record


# def test_current_directory():
#     # path = pytest.__pytestPDB._config.rootdir
#     # path = py.path.local
#     # path = config.Config.rootdir
#     # print(path)
#     print(os.getcwd())
#     print(sys.path[0])
from ecgai_drawing.enums.ecg_lead_name import LeadName
from ecgai_drawing.models.ecg_lead import Lead
from ecgai_drawing.models.ecg_leads import Leads
from tests.test_helper import single_valid_record_path_name, setup_test_record_data


# @pytest.mark.asyncio
def test_create_ecg_leads():
    # try:
    random_signals = np.random.random(50)
    test_signal: List[float] = random_signals.tolist()
    test_lead1 = Lead.create("II", test_signal)
    test_lead2 = Lead.create("III", test_signal)
    test_lead3 = Lead.create("aVF", test_signal)
    test_lead4 = Lead.create("aVL", test_signal)
    test_lead5 = Lead.create("V6", test_signal)
    test_lead6 = Lead.create("V1", test_signal)
    test_leads = [
        test_lead1,
        test_lead2,
        test_lead3,
        test_lead4,
        test_lead5,
        test_lead6,
    ]
    record = Leads.create(record_name="test1", sample_rate=500, leads=test_leads)
    assert type(record) is Leads
    assert len(record.leads) == 6


def test_create_ecg_lead_record():
    random_signals = np.random.random(50)
    test_signal: List[float] = random_signals.tolist()
    test_lead = Lead.create("V6", test_signal)
    assert test_lead.lead_name == LeadName.V6


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
# @pytest.mark.asyncio
def test_read_from_json(record_path_name):
    record = setup_test_record_data(path_name=record_path_name)
    assert type(record) is Leads


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
# @pytest.mark.asyncio
def test_write_to_json(record_path_name, tmp_path):
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    assert type(ecg_leads) is Leads
    with pytest.raises(NotImplementedError):
        ecg_leads.to_json()