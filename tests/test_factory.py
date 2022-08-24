import json
import pathlib

from numpy import ndarray

from definitions import ROOT_DIR
from ecgai_drawing.images import convert_from_bytes, load_image, save_image
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
    "tests/test_data/00001_hr.json",
}


def setup_test_record_data(path_name: str) -> Leads:
    # record_path = os.path.abspath(os.path.join(path_name))
    record_path = pathlib.Path(ROOT_DIR, path_name)
    # record = Leads()
    # with open(record_path) as f:
    #     record.from_json(f.read())
    print("the file path for load record is " + str(record_path))
    with open(record_path) as json_file:
        data = json.load(json_file)
    record = Leads.from_json(data)
    assert type(record) is Leads
    return record


# def copy_file(source:Path, destination):
#     dest = Path('dest')
#     src = Path('src')
#     dest.write_bytes(src.read_bytes())  # for binary files
#     dest.write_text(src.read_text())  # for text files


# from ecgai_drawing_ecg_grpc.ecg_drawing import EcgPlotRequest
BASE_IMAGE_NAME = "base_image.png"
BYTE_IMAGE_NAME = "byte_image.png"
COLOR_WITHOUT_GRID_NAME = "color_without_grid.png"
COLOR_WITH_GRID_NAME = "color_with_grid.png"
GREY_SCALE_WITH_GRID_NAME = "grey_scale_with_grid.png"
GREY_SCALE_WITHOUT_GRID_NAME = "grey_scale_without_grid.png"
MASK_NAME = "mask.png"


def data_directory() -> pathlib.Path:
    file_path = pathlib.Path(ROOT_DIR, "tests/test_data")
    print(file_path)
    return file_path


def save_byte_image_to_test_directory(byte_image: bytes, image_name: str, path: pathlib.Path):
    image = convert_from_bytes(byte_image)
    save_image(image=image, image_name=image_name, save_path=str(path))


def save_base_image_to_test_directory(image: ndarray, path: pathlib.Path):
    save_image(image=image, image_name=BASE_IMAGE_NAME, save_path=str(path))


def get_image_path(name, path):
    return pathlib.Path(path, name)


def load_base_image(image_name: str):
    image = load_image(image_name=image_name, image_path=data_directory())
    return image


#
# def save_draw_ecg_plot_response_to_file(draw_response, tmp_path):
#     file_name = "test_00001.ecgai"
#     file_path = os.path.join(tmp_path, file_name)
#     with open(file_path, "w") as f:
#         f.write(draw_response.to_json())
#     assert os.path.isfile(file_path) is True
#     return file_path
#
