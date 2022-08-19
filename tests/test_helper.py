import json
import os

from ecgai_drawing.models.ecg_leads import Leads

# from definitions import ROOT_DIR

valid_record_path_name = {
    "test_data/00001_hr.json",
    "test_data/00002_hr.json",
    "test_data/00003_hr.json",
    "test_data/00004_hr.json",
    "test_data/00005_hr.json",
    "test_data/00006_hr.json",
    "test_data/00007_hr.json",
    "test_data/00008_hr.json",
    "test_data/00009_hr.json",
    "test_data/00010_hr.json",
}

single_valid_record_path_name = {
    "test_data/00001_hr.json",
}


def setup_test_record_data(path_name: str) -> Leads:
    record_path = os.path.abspath(os.path.join(path_name))
    # record = Leads()
    # with open(record_path) as f:
    #     record.from_json(f.read())
    print("the file path for load record is " + record_path)
    with open(record_path) as json_file:
        data = json.load(json_file)
    record = Leads.from_json(data)
    assert type(record) is Leads
    return record
