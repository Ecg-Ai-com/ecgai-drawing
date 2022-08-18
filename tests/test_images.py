import os

import numpy as np

from ecgai_drawing.images import (
    convert_from_bytes,
    convert_to_bytes,
    load_image,
    save_image,
)

# from matplotlib.testing.compare import compare_images


# from ecgai_drawing_ecg_grpc.ecg_drawing import DrawEcgPlotResponse


def image_name() -> str:
    return "colour_image.png"


def image_path() -> str:
    return os.path.abspath("test_data")


def create_byte_image(byte_image, tmp_path):
    byte_image_name = "byte_image.png"
    image_array = convert_from_bytes(byte_image)
    save_image(image=image_array, image_name=byte_image_name, save_path=str(tmp_path))
    byte_image_file_name = os.path.join(tmp_path, byte_image_name)
    print(byte_image_file_name)
    return byte_image_file_name


def create_base_image(tmp_path):
    base_image_name = "base_image.png"
    image = load_image(image_name=image_name(), image_path=image_path())
    save_image(image=image, image_name=base_image_name, save_path=str(tmp_path))
    byte_image = convert_to_bytes(image)
    base_image_file_name = os.path.join(tmp_path, base_image_name)
    print("")
    print(base_image_file_name)
    return base_image_file_name, byte_image


#
# def save_draw_ecg_plot_response_to_file(draw_response, tmp_path):
#     file_name = "test_00001.ecgai"
#     file_path = os.path.join(tmp_path, file_name)
#     with open(file_path, "w") as f:
#         f.write(draw_response.to_json())
#     assert os.path.isfile(file_path) is True
#     return file_path
#


def test_open_image():
    image = load_image(image_name=image_name(), image_path=image_path())
    isinstance(image, np.ndarray)


#
#
# def test_convert_to_bytes():
#     image = load_image(image_name=image_name(), image_path=image_path())
#     byte_image = convert_to_bytes(image)
#     isinstance(byte_image, bytes)
#
#
# def test_convert_from_bytes():
#     image = load_image(image_name=image_name(), image_path=image_path())
#     byte_image = convert_to_bytes(image)
#     image_array = convert_from_bytes(byte_image)
#     isinstance(image_array, np.ndarray)
#
#
# def test_convert_from_bytes_write_to_image_file(tmp_path):
#     # arrange
#     base_image_file_name, byte_image = create_base_image(tmp_path)
#     # act
#     byte_image_file_name = create_byte_image(byte_image, tmp_path)
#     # assert
#     number_of_files = len(os.listdir(tmp_path))
#     assert number_of_files == 2
#     compare_images(expected=base_image_file_name, actual=byte_image_file_name, tol=0)
#
#
# # def test_convert_from_bytes_save_to_protobuf_file(tmp_path):
# #     # arrange
# #     base_image_file_name, byte_image = create_base_image(tmp_path)
# #
# #     # act
# #     draw_response = DrawEcgPlotResponse(transaction_id='1',
# #     record_name='name', file_name='filename', image=byte_image)
# #
# #     # assert
# #     isinstance(draw_response, DrawEcgPlotResponse)
# #     assert len(draw_response.image) != 0
# #
# #
# # def test_convert_from_bytes_to_protobuf_write_to_image_file(tmp_path):
# #     # arrange
# #     base_image_file_name, byte_image = create_base_image(tmp_path)
# #
# #     # act
# #     draw_response = DrawEcgPlotResponse(transaction_id='1', record_name='name'
# #     , file_name='filename', image=byte_image)
# #     byte_image_file_name = create_byte_image(draw_response.image, tmp_path)
# #
# #     # assert
# #     number_of_files = len(os.listdir(tmp_path))
# #     assert number_of_files == 2
# #     compare_images(expected=base_image_file_name, actual=byte_image_file_name, tol=0)
# #
# #
# # def test_convert_from_bytes_save_to_protobuf_file_open_write_to_image_file(tmp_path):
# #     # arrange
# #     base_image_file_name, byte_image = create_base_image(tmp_path)
# #
# #     # act
# #     draw_response = DrawEcgPlotResponse(transaction_id='1', record_name='name',
# #     file_name='filename', image=byte_image)
# #
# #     draw_response_file_path = save_draw_ecg_plot_response_to_file(draw_response, tmp_path)
# #
# #     opened_draw_response = DrawEcgPlotResponse()
# #     with open(draw_response_file_path, "r") as f:
# #         opened_draw_response.from_json(f.read())
# #
# #     byte_image_file_name = create_byte_image(opened_draw_response.image, tmp_path)
# #
# #     # assert
# #     number_of_files = len(os.listdir(tmp_path))
# #     assert number_of_files == 3
# #     compare_images(expected=base_image_file_name, actual=byte_image_file_name, tol=0)
