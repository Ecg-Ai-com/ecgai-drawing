import os

import numpy as np
from matplotlib.testing.compare import compare_images

from ecgai_drawing.images import convert_from_bytes, convert_to_bytes, load_image
from tests.test_factory import (
    BASE_IMAGE_NAME,
    BYTE_IMAGE_NAME,
    COLOR_WITHOUT_GRID_NAME,
    data_directory,
    get_image_path,
    load_base_image,
    save_base_image_to_test_directory,
    save_byte_image_to_test_directory,
)


def test_open_image():
    image = load_image(image_name=COLOR_WITHOUT_GRID_NAME, image_path=data_directory())
    isinstance(image, np.ndarray)


def test_convert_to_bytes():
    image = load_image(image_name=COLOR_WITHOUT_GRID_NAME, image_path=data_directory())
    byte_image = convert_to_bytes(image)
    isinstance(byte_image, bytes)


def test_convert_from_bytes():
    image = load_image(image_name=COLOR_WITHOUT_GRID_NAME, image_path=data_directory())
    byte_image = convert_to_bytes(image)
    image_array = convert_from_bytes(byte_image)
    isinstance(image_array, np.ndarray)


def test_convert_from_bytes_write_to_image_file(tmp_path):
    # arrange
    image = load_base_image(COLOR_WITHOUT_GRID_NAME)
    save_base_image_to_test_directory(image=image, path=tmp_path)
    base_image_file_name = get_image_path(name=BASE_IMAGE_NAME, path=tmp_path)
    byte_image = convert_to_bytes(image)
    # act
    save_byte_image_to_test_directory(byte_image=byte_image, image_name=BYTE_IMAGE_NAME, path=tmp_path)
    byte_image_file_name = get_image_path(name=BYTE_IMAGE_NAME, path=tmp_path)
    # assert

    compare_images(expected=str(base_image_file_name), actual=str(byte_image_file_name), tol=0)
    number_of_files = len(os.listdir(tmp_path))
    assert number_of_files == 2


# def test_convert_from_bytes_save_to_protobuf_file(tmp_path):
#     # arrange
#     base_image_file_name, byte_image = create_base_image(tmp_path)
#
#     # act
#     draw_response = DrawEcgPlotRequest(transaction_id='1',
#     record_name='name', file_name='filename', image=byte_image)
#
#     # assert
#     isinstance(draw_response, DrawEcgPlotRequest)
#     assert len(draw_response.image) != 0
#
#
# def test_convert_from_bytes_to_protobuf_write_to_image_file(tmp_path):
#     # arrange
#     base_image_file_name, byte_image = create_base_image(tmp_path)
#
#     # act
#     draw_response = DrawEcgPlotRequest(transaction_id='1', record_name='name'
#     , file_name='filename', image=byte_image)
#     byte_image_file_name = create_byte_image(draw_response.image, tmp_path)
#
#     # assert
#     number_of_files = len(os.listdir(tmp_path))
#     assert number_of_files == 2
#     compare_images(expected=base_image_file_name, actual=byte_image_file_name, tol=0)
#
#
# def test_convert_from_bytes_save_to_protobuf_file_open_write_to_image_file(tmp_path):
#     # arrange
#     base_image_file_name, byte_image = create_base_image(tmp_path)
#
#     # act
#     draw_response = DrawEcgPlotRequest(transaction_id='1', record_name='name',
#     file_name='filename', image=byte_image)
#
#     draw_response_file_path = save_draw_ecg_plot_response_to_file(draw_response, tmp_path)
#
#     opened_draw_response = DrawEcgPlotRequest()
#     with open(draw_response_file_path, "r") as f:
#         opened_draw_response.from_json(f.read())
#
#     byte_image_file_name = create_byte_image(opened_draw_response.image, tmp_path)
#
#     # assert
#     number_of_files = len(os.listdir(tmp_path))
#     assert number_of_files == 3
#     compare_images(expected=base_image_file_name, actual=byte_image_file_name, tol=0)
