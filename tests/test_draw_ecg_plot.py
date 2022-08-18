import os
import uuid
from json import JSONEncoder

import numpy as np
import pytest

from ecgai_drawing.draw_ecg_plot import DrawEcgPlot
from ecgai_drawing.ecg_plot_response import DrawEcgPlotResponse
from ecgai_drawing.enums.artifact import Artifact
from ecgai_drawing.enums.color_style import ColorStyle
from ecgai_drawing.enums.show_grid import ShowGrid
from ecgai_drawing.images import save_image
from tests.test_helper import setup_test_record_data, single_valid_record_path_name

# @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
# def test_create_ecg_plotter_request_with_defaults(record_path_name): # arrange
# ecg_leads = setup_test_record_data(path_name=record_path_name) transaction_id =
# uuid.uuid4().hex # act ecg_plotter_request = DrawEcgPlotRequest(
# transaction_id=transaction_id, color_style=ColorStyle.COLOR,
# artifact=Artifact.NONE, ecg=ecg_leads)
#
#     # assert
#     assert type(ecg_plotter_request) is DrawEcgPlotRequest
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
#     ecg_plotter_request = DrawEcgPlotRequest(
#         transaction_id=transaction_id,
#         ecg=ecg,
#         color_style=ColorStyle.BINARY,
#         show_grid=False,
#         artifact=Artifact.SALT_AND_PEPPER,
#     )
#
#     # assert
#     assert type(ecg_plotter_request) is DrawEcgPlotRequest
#     assert ecg_plotter_request.transaction_id is transaction_id
#     assert ecg_plotter_request.color_style is ColorStyle.BINARY
#     assert ecg_plotter_request.show_grid is False
#     assert ecg_plotter_request.artifact is Artifact.SALT_AND_PEPPER


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_color_no_grid_salt_and_peper(
    record_path_name, tmp_path
):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex
    parameters = DrawEcgPlotResponse(
        transaction_id=transaction_id,
        record_name="record name test",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.color,
        show_grid=ShowGrid.false,
        artifact=Artifact.salt_and_pepper,
        file_name="00001",
    )

    draw_plot = DrawEcgPlot(parameters)
    # Act
    image = draw_plot.handle()
    save_image(image=image, image_name="nparray_test.png", save_path=str(tmp_path))

    # assert type(draw_response) is DrawEcgPlotResponse
    #
    # read_buffer = base64.b64decode(draw_response.image)
    # image_1 = np.asarray(bytearray(read_buffer))
    # read_image = cv2.imdecode(image_1, cv2.IMREAD_UNCHANGED)
    #
    # # read_image = cv2.imdecode(draw_response.image, cv2.IMREAD_UNCHANGED)
    # save_image(image=read_image, image_name="buffer_test.png", save_path=str(
    # tmp_path)) Assert
    number_of_files = len(os.listdir(tmp_path))
    assert number_of_files == 1


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_color_with_grid(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex

    parameters = DrawEcgPlotResponse(
        transaction_id=transaction_id,
        record_name="record name test",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.color,
        show_grid=ShowGrid.true,
        artifact=Artifact.none,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot(plot_parameters=parameters)
    # Act
    image = draw_plot.handle()
    save_image(image=image, image_name="nparray_test.png", save_path=str(tmp_path))

    # Assert
    number_of_files = len(os.listdir(tmp_path))
    assert number_of_files == 1


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_color_no_grid(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex

    parameters = DrawEcgPlotResponse(
        transaction_id=transaction_id,
        record_name="record name test",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.color,
        show_grid=ShowGrid.false,
        artifact=Artifact.none,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot(parameters)
    # Act
    image = draw_plot.handle()
    save_image(image=image, image_name="nparray_test.png", save_path=str(tmp_path))

    # Assert
    number_of_files = len(os.listdir(tmp_path))
    assert number_of_files == 1


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_black_and_white_with_grid(
    record_path_name, tmp_path
):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex

    parameters = DrawEcgPlotResponse(
        transaction_id=transaction_id,
        record_name="record name test",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.black_and_white,
        show_grid=ShowGrid.true,
        artifact=Artifact.none,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot(parameters)
    # Act
    image = draw_plot.handle()
    save_image(image=image, image_name="nparray_test.png", save_path=str(tmp_path))

    # Assert
    number_of_files = len(os.listdir(tmp_path))
    assert number_of_files == 1


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_black_and_white_with_grid_salt(
    record_path_name, tmp_path
):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex

    parameters = DrawEcgPlotResponse(
        transaction_id=transaction_id,
        record_name="record name test",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.black_and_white,
        show_grid=ShowGrid.true,
        artifact=Artifact.salt,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot(parameters)

    # Act
    image = draw_plot.handle()
    save_image(image=image, image_name="nparray_test.png", save_path=str(tmp_path))

    # Assert
    number_of_files = len(os.listdir(tmp_path))
    assert number_of_files == 1


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_black_and_white_with_grid_salt_and_peper(
    record_path_name, tmp_path
):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex

    parameters = DrawEcgPlotResponse(
        transaction_id=transaction_id,
        record_name="record name test",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.black_and_white,
        show_grid=ShowGrid.true,
        artifact=Artifact.salt_and_pepper,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot(parameters)

    # Act
    image = draw_plot.handle()
    save_image(image=image, image_name="nparray_test.png", save_path=str(tmp_path))

    # Assert
    number_of_files = len(os.listdir(tmp_path))
    assert number_of_files == 1


@pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
def test_create_draw_ecg_plot_with_mask(record_path_name, tmp_path):
    # Arrange
    ecg_leads = setup_test_record_data(path_name=record_path_name)
    transaction_id = uuid.uuid4().hex

    parameters = DrawEcgPlotResponse(
        transaction_id=transaction_id,
        record_name="record name test",
        sample_rate=ecg_leads.sample_rate,
        ecg_leads=ecg_leads,
        color_style=ColorStyle.mask,
        show_grid=ShowGrid.true,
        artifact=Artifact.none,
        file_name="00001",
    )
    draw_plot = DrawEcgPlot(parameters)

    # Act
    image = draw_plot.handle()
    save_image(image=image, image_name="mask.png", save_path=str(tmp_path))

    # Assert
    number_of_files = len(os.listdir(tmp_path))
    assert number_of_files == 1


# @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
# def test_create_draw_ecg_plot_request_and_save_as_json( record_path_name, tmp_path
# ): # Arrange ecg_leads = setup_test_record_data(path_name=record_path_name)
# draw_request = DrawEcgPlotRequestOld.create(ecg_leads=ecg_leads,
# color_style=ColorStyle.color, show_grid=ShowGrid.true,
# artifact=Artifact.salt_and_pepper) draw_plot = DrawEcgPlotResponse(
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
# DrawEcgPlotResponse(draw_request=draw_request)
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
