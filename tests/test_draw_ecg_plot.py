import pathlib
import uuid
from json import JSONEncoder

import numpy as np
import pytest
from matplotlib.testing.compare import compare_images

from ecgai_drawing.draw_ecg_plot import DrawEcgPlot
from ecgai_drawing.ecg_plot_request import EcgPlotRequest
from ecgai_drawing.enums.artifact import Artifact
from ecgai_drawing.enums.color_style import ColorStyle
from tests.test_factory import (
    BASE_IMAGE_NAME,
    COLOR_WITH_GRID_NAME,
    COLOR_WITHOUT_GRID_NAME,
    GREY_SCALE_WITH_GRID_NAME,
    GREY_SCALE_WITHOUT_GRID_NAME,
    MASK_NAME,
    get_image_path,
    load_base_image,
    save_base_image_to_test_directory,
    save_byte_image_to_test_directory,
    setup_test_record_data,
    single_valid_record_path_name,
)


def count_files(path: pathlib.Path, name: str = "*.*"):
    return len(list(pathlib.Path(path).glob(name)))


def image_name(draw_response) -> str:
    name = draw_response.file_name + draw_response.file_extension
    return name


# @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
# def test_create_ecg_plotter_request_with_defaults(record_path_name): # arrange
# ecg_leads = setup_test_record_data(path_name=record_path_name) transaction_id =
# uuid.uuid4().hex # act ecg_plotter_request = EcgPlotRequest(
# transaction_id=transaction_id, color_style=ColorStyle.COLOR,
# artifact=Artifact.NONE, ecg=ecg_leads)
#
#     # assert

#     assert type(ecg_plotter_request) is EcgPlotRequest
#     assert ecg_plotter_request.transaction_id is transaction_id
#     assert ecg_plotter_request.color_style is ColorStyle.COLOR
#     assert ecg_plotter_request.show_grid is False
#     assert ecg_plotter_request.artifact is Artifact.NONE


# @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
# def test_create_ecg_plotter_request_with_values(record_path_name):
#     # arrange
#     ecg = setup_test_record_data(path_name=record_path_name)
#     transaction_id = uuid.uuid4().hex
#     # act
#     ecg_plotter_request = EcgPlotRequest(
#         transaction_id=transaction_id,
#         ecg=ecg,
#         color_style=ColorStyle.BINARY,
#         show_grid=False,
#         artifact=Artifact.SALT_AND_PEPPER,
#     )
#
#     # assert
#     assert type(ecg_plotter_request) is EcgPlotRequest
#     assert ecg_plotter_request.transaction_id is transaction_id
#     assert ecg_plotter_request.color_style is ColorStyle.BINARY
#     assert ecg_plotter_request.show_grid is False
#     assert ecg_plotter_request.artifact is Artifact.SALT_AND_PEPPER


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_color_no_grid_salt_and_peper(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex
    request = EcgPlotRequest.create(
        transaction_id=transaction_id,
        record_name="ECG 12 lead",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.color,
        show_grid=False,
        artifact=Artifact.salt_and_pepper,
        file_name="00001",
    )

    draw_plot = DrawEcgPlot()
    # Act
    draw_response = draw_plot.handle(request)

    # Assert
    file_name = image_name(draw_response)
    save_byte_image_to_test_directory(byte_image=draw_response.image, image_name=file_name, path=tmp_path)

    count = count_files(tmp_path, file_name)
    assert file_name == "sp_00001.png"
    assert count == 1

    # print(len(l))


#
# def convert_byte_to_image_test(draw_response, tmp_path):
#     image = convert_from_bytes(draw_response.image)
#     save_image(image=image, image_name=draw_response.file_name + draw_response.file_extension,
#     save_path=str(tmp_path))
#     byte_image = os.path.join(tmp_path, draw_response.file_name + draw_response.file_extension)
#     base_image = copy_base_image(tmp_path)
#     compare_images(expected=base_image, actual=byte_image, tol=0)
#     number_of_files = len(os.listdir(tmp_path))
#     assert number_of_files == 2

#
# def copy_base_image(tmp_path):
#     my_file = pathlib.Path(ROOT_DIR, "tests/test_data/color_without_grid.png")
#     shutil.copy(my_file, tmp_path)  # For Python 3.8+.
#     base_image = os.path.join(tmp_path, "color_without_grid.png")
#     return base_image


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_color_with_grid(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex

    request = EcgPlotRequest.create(
        transaction_id=transaction_id,
        record_name="ECG 12 lead",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.color,
        show_grid=True,
        artifact=Artifact.artifact_unspecified,
        file_name="00001",
    )

    draw_plot = DrawEcgPlot()
    # Act
    draw_response = draw_plot.handle(request)

    # Assert
    file_name = image_name(draw_response)
    save_byte_image_to_test_directory(byte_image=draw_response.image, image_name=file_name, path=tmp_path)

    count = count_files(tmp_path, file_name)
    assert file_name == "00001.png"
    assert count == 1


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_color_no_grid(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex

    request = EcgPlotRequest.create(
        transaction_id=transaction_id,
        record_name="ECG 12 lead",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.color,
        show_grid=False,
        artifact=Artifact.artifact_unspecified,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot()
    # Act
    draw_response = draw_plot.handle(request)

    # Assert
    file_name = image_name(draw_response)
    save_byte_image_to_test_directory(byte_image=draw_response.image, image_name=file_name, path=tmp_path)

    count = count_files(tmp_path, file_name)
    assert file_name == "00001.png"
    assert count == 1


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_grey_scale_with_grid(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex

    request = EcgPlotRequest.create(
        transaction_id=transaction_id,
        record_name="ECG 12 lead",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.grey_scale,
        show_grid=True,
        artifact=Artifact.artifact_unspecified,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot()
    # Act
    draw_response = draw_plot.handle(request)

    # Assert
    file_name = image_name(draw_response)
    save_byte_image_to_test_directory(byte_image=draw_response.image, image_name=file_name, path=tmp_path)

    count = count_files(tmp_path, file_name)
    assert file_name == "gs_00001.png"
    assert count == 1


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_grey_scale_without_grid(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex

    request = EcgPlotRequest.create(
        transaction_id=transaction_id,
        record_name="ECG 12 lead",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.grey_scale,
        show_grid=False,
        artifact=Artifact.artifact_unspecified,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot()
    # Act
    draw_response = draw_plot.handle(request)

    # Assert
    file_name = image_name(draw_response)
    save_byte_image_to_test_directory(byte_image=draw_response.image, image_name=file_name, path=tmp_path)

    count = count_files(tmp_path, file_name)
    assert file_name == "gs_00001.png"
    assert count == 1


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_black_and_white_with_grid_salt(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex

    request = EcgPlotRequest.create(
        transaction_id=transaction_id,
        record_name="ECG 12 lead",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.black_and_white,
        show_grid=True,
        artifact=Artifact.salt,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot()
    # Act
    draw_response = draw_plot.handle(request)

    # Assert
    file_name = image_name(draw_response)
    save_byte_image_to_test_directory(byte_image=draw_response.image, image_name=file_name, path=tmp_path)

    count = count_files(tmp_path, file_name)
    assert file_name == "bw_s_00001.png"
    assert count == 1


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_black_and_white_with_grid_salt_and_peper(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex

    request = EcgPlotRequest.create(
        transaction_id=transaction_id,
        record_name="ECG 12 lead",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.black_and_white,
        show_grid=True,
        artifact=Artifact.salt_and_pepper,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot()
    # Act
    draw_response = draw_plot.handle(request)

    # Assert
    file_name = image_name(draw_response)
    save_byte_image_to_test_directory(byte_image=draw_response.image, image_name=file_name, path=tmp_path)

    count = count_files(tmp_path, file_name)
    assert file_name == "bw_sp_00001.png"
    assert count == 1


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_mask(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex

    request = EcgPlotRequest.create(
        transaction_id=transaction_id,
        record_name="ECG 12 lead",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.mask,
        show_grid=False,
        artifact=Artifact.artifact_unspecified,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot()
    # Act
    draw_response = draw_plot.handle(request)

    # Assert
    file_name = image_name(draw_response)
    save_byte_image_to_test_directory(byte_image=draw_response.image, image_name=file_name, path=tmp_path)

    count = count_files(tmp_path, file_name)
    assert file_name == "mask_00001.png"
    assert count == 1


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_color_no_grid_compare_against_base_image(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)

    image = load_base_image(COLOR_WITHOUT_GRID_NAME)
    save_base_image_to_test_directory(image=image, path=tmp_path)
    base_image_file_name = get_image_path(name=BASE_IMAGE_NAME, path=tmp_path)

    transaction_id = uuid.uuid4().hex

    request = EcgPlotRequest.create(
        transaction_id=transaction_id,
        record_name="ECG 12 lead",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.color,
        show_grid=False,
        artifact=Artifact.artifact_unspecified,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot()
    # Act
    draw_response = draw_plot.handle(request)

    # Assert
    file_name = image_name(draw_response)
    save_byte_image_to_test_directory(byte_image=draw_response.image, image_name=file_name, path=tmp_path)

    image_file_name = get_image_path(name=file_name, path=tmp_path)
    compare_images(expected=str(base_image_file_name), actual=str(image_file_name), tol=0)
    count = count_files(tmp_path)

    assert count == 2


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_color_with_grid_compare_against_base_image(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)

    image = load_base_image(COLOR_WITH_GRID_NAME)
    save_base_image_to_test_directory(image=image, path=tmp_path)
    base_image_file_name = get_image_path(name=BASE_IMAGE_NAME, path=tmp_path)

    transaction_id = uuid.uuid4().hex

    request = EcgPlotRequest.create(
        transaction_id=transaction_id,
        record_name="ECG 12 lead",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.color,
        show_grid=True,
        artifact=Artifact.artifact_unspecified,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot()
    # Act
    draw_response = draw_plot.handle(request)

    # Assert
    file_name = image_name(draw_response)
    save_byte_image_to_test_directory(byte_image=draw_response.image, image_name=file_name, path=tmp_path)

    image_file_name = get_image_path(name=file_name, path=tmp_path)
    compare_images(expected=str(base_image_file_name), actual=str(image_file_name), tol=0)
    count = count_files(tmp_path)

    assert count == 2


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_grey_scale_with_grid_compare_against_base_image(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)

    image = load_base_image(GREY_SCALE_WITH_GRID_NAME)
    save_base_image_to_test_directory(image=image, path=tmp_path)
    base_image_file_name = get_image_path(name=BASE_IMAGE_NAME, path=tmp_path)

    transaction_id = uuid.uuid4().hex

    request = EcgPlotRequest.create(
        transaction_id=transaction_id,
        record_name="ECG 12 lead",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.grey_scale,
        show_grid=True,
        artifact=Artifact.artifact_unspecified,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot()
    # Act
    draw_response = draw_plot.handle(request)

    # Assert
    file_name = image_name(draw_response)
    save_byte_image_to_test_directory(byte_image=draw_response.image, image_name=file_name, path=tmp_path)

    image_file_name = get_image_path(name=file_name, path=tmp_path)
    compare_images(expected=str(base_image_file_name), actual=str(image_file_name), tol=0)
    count = count_files(tmp_path)

    assert count == 2


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_grey_scale_without_grid_compare_against_base_image(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)

    image = load_base_image(GREY_SCALE_WITHOUT_GRID_NAME)
    save_base_image_to_test_directory(image=image, path=tmp_path)
    base_image_file_name = get_image_path(name=BASE_IMAGE_NAME, path=tmp_path)

    transaction_id = uuid.uuid4().hex

    request = EcgPlotRequest.create(
        transaction_id=transaction_id,
        record_name="ECG 12 lead",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.grey_scale,
        show_grid=False,
        artifact=Artifact.artifact_unspecified,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot()
    # Act
    draw_response = draw_plot.handle(request)

    # Assert
    file_name = image_name(draw_response)
    save_byte_image_to_test_directory(byte_image=draw_response.image, image_name=file_name, path=tmp_path)

    image_file_name = get_image_path(name=file_name, path=tmp_path)
    compare_images(expected=str(base_image_file_name), actual=str(image_file_name), tol=0)
    count = count_files(tmp_path)

    assert count == 2


# noinspection DuplicatedCode
@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_mask_compare_against_base_image(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)

    image = load_base_image(MASK_NAME)
    save_base_image_to_test_directory(image=image, path=tmp_path)
    base_image_file_name = get_image_path(name=BASE_IMAGE_NAME, path=tmp_path)

    transaction_id = uuid.uuid4().hex

    request = EcgPlotRequest.create(
        transaction_id=transaction_id,
        record_name="ECG 12 lead",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.mask,
        show_grid=False,
        artifact=Artifact.artifact_unspecified,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot()
    # Act
    draw_response = draw_plot.handle(request)

    # Assert
    file_name = image_name(draw_response)
    save_byte_image_to_test_directory(byte_image=draw_response.image, image_name=file_name, path=tmp_path)

    image_file_name = get_image_path(name=file_name, path=tmp_path)
    compare_images(expected=str(base_image_file_name), actual=str(image_file_name), tol=0)
    count = count_files(tmp_path)

    assert count == 2


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_mask_grid_true_overridden_to_false_compare_against_base_image(
    record_path_name, tmp_path
):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)

    image = load_base_image(MASK_NAME)
    save_base_image_to_test_directory(image=image, path=tmp_path)
    base_image_file_name = get_image_path(name=BASE_IMAGE_NAME, path=tmp_path)

    transaction_id = uuid.uuid4().hex

    request = EcgPlotRequest.create(
        transaction_id=transaction_id,
        record_name="ECG 12 lead",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.mask,
        show_grid=True,
        artifact=Artifact.artifact_unspecified,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot()
    # Act
    draw_response = draw_plot.handle(request)

    # Assert
    file_name = image_name(draw_response)
    save_byte_image_to_test_directory(byte_image=draw_response.image, image_name=file_name, path=tmp_path)

    image_file_name = get_image_path(name=file_name, path=tmp_path)
    compare_images(expected=str(base_image_file_name), actual=str(image_file_name), tol=0)
    count = count_files(tmp_path)

    assert count == 2


# @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
# def test_create_draw_ecg_plot_request_and_save_as_json( record_path_name, tmp_path
# ): # Arrange ecg_leads = setup_test_record_data(path_name=record_path_name)
# draw_request = DrawEcgPlotRequestOld.create(ecg_leads=ecg_leads,
# color_style=ColorStyle.color, show_grid=ShowGrid.true,
# artifact=Artifact.salt_and_pepper) draw_plot = EcgPlotRequest(
# draw_request=draw_request) json_value = draw_plot.handle() file_name =
# 'save_as_json.json' file_path = os.path.join(tmp_path, file_name) with open(
# file_path, 'w') as outfile: json.dump(json_value, outfile, cls=NumpyArrayEncoder)
#
#         # encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
#     assert os.path.isfile(file_path) is True


# @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
# def test_create_draw_ecg_plot_response_save_as_json(
#         record_path_name, tmp_path
# ):
#     # noinspection DuplicatedCode
#     ecg_leads = setup_test_record_data(path_name=record_path_name)
#
# transaction_id = uuid.uuid4().hex draw_request = DrawEcgPlotRequestOld.create(
# transaction_id=transaction_id, ecg_leads=ecg_leads, color_style=ColorStyle.color,
# show_grid=Grid.true, artifact=Artifact.salt_and_pepper) draw_ecg =
# EcgPlotRequest(draw_request=draw_request)
#
#     draw_response = draw_ecg.handle()
#     json_value = draw_response.to_json()
#     file_name = 'response.json'
#     file_path = os.path.join(tmp_path, file_name)
#     print(file_path)
#     with open(file_path, 'w') as outfile:
#         json.dump(json_value, outfile)
#     assert os.path.isfile(file_path) is True


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)
