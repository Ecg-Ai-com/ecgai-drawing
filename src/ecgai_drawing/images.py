import base64
import os

import cv2
import numpy as np
import skimage
from numpy import ndarray


def load_image(image_name: str, image_path: str, as_gray: bool = False) -> ndarray:
    file_name = os.path.join(image_path, image_name)
    return skimage.io.imread(fname=file_name, as_gray=as_gray)


def save_image_as_ubyte(image: ndarray, image_name: str, save_path: str):
    byte_image = skimage.img_as_ubyte(image)
    save_image(image=byte_image, image_name=image_name, save_path=save_path)


def save_image_as_bool(image: ndarray, image_name: str, save_path: str):
    byte_image = skimage.img_as_bool(image)
    save_image(image=byte_image, image_name=image_name, save_path=save_path)


def save_image(image: ndarray, image_name: str, save_path: str):
    file_name = os.path.join(save_path, image_name)
    skimage.io.imsave(fname=file_name, arr=image)


def convert_to_mask(image: ndarray) -> ndarray:
    image = convert_to_binary(image=image)
    return skimage.util.invert(image)


def convert_to_binary(image: ndarray) -> ndarray:
    thresh = skimage.filters.threshold_isodata(image)
    return image > thresh


def convert_to_black_and_white(image: ndarray):
    return skimage.color.rgb2gray(image)


def convert_to_bytes(image: ndarray) -> bytes:
    return cv2.imencode(".png", image)[1].tobytes()


def convert_from_bytes(stream: bytes) -> ndarray:
    imgage = np.frombuffer(stream, dtype=np.uint8)  # <class 'numpy.ndarray'>

    return cv2.imdecode(imgage, cv2.IMREAD_UNCHANGED)


def convert_to_base64_string(image: ndarray) -> str:
    image_array = cv2.imencode(".png", image)[1]
    return base64.b64encode(image_array).decode()


# def create_binary_image(image_name: str, image_path: str) -> ndarray:
#     image = load_image(image_name=image_name, image_path=image_path, as_gray=True)
#     thresh = threshold_isodata(image)
#     return image > thresh

# def create_binary_image(image: ndarray) -> ndarray:
#     thresh = threshold_isodata(image)
#     return image > thresh
#
#
# def convert_to_grey_scale(image: ndarray) -> ndarray:
#     image = rgba2rgb(image)
#     return rgb2gray(image)
#
#
def convert_from_rgba_to_rgb(image: ndarray) -> ndarray:
    return skimage.color.rgba2rgb(image)


#
#
# #
# # def create_bool_image(image: ndarray):
# #     bool_image = img_as_bool(image=image)
# #     return bool_image
#
#
# def invert_image(image: ndarray) -> ndarray:
#     return util.invert(image)
#
#


def add_salt_and_pepper_to_image(image: ndarray) -> ndarray:
    return skimage.util.random_noise(image=image, mode="s&p")


def add_salt_to_image(image: ndarray) -> ndarray:
    return skimage.util.random_noise(image=image, mode="salt")


def add_pepper_to_image(image: ndarray) -> ndarray:
    return skimage.util.random_noise(image=image, mode="pepper")
