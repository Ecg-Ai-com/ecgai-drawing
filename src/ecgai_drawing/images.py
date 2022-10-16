import base64
import os
from pathlib import Path

import cv2
import numpy as np
import skimage
from numpy import ndarray

DEFAULT_FILE_EXTENSION = ".png"


def load_image(image_name: str, image_path: Path) -> ndarray:
    file_name = os.path.join(image_path, image_name)
    print("the file path for load is " + file_name)
    # return skimage.io.imread(fname=file_name)
    # TODO cv.imread or cv.imwrite is changing the colour of the ecg line from red to blue, find solution
    return cv2.imread(filename=file_name, flags=cv2.IMREAD_UNCHANGED)


def save_image_as_ubyte(image: ndarray, image_name: str, save_path: str):
    byte_image = skimage.img_as_ubyte(image)
    save_image(image=byte_image, image_name=image_name, save_path=save_path)


# def save_image_as_bool(image: ndarray, COLOR_WITHOUT_GRID_NAME: str, save_path: str):
#     byte_image = skimage.img_as_bool(image)
#     save_image(image=byte_image, COLOR_WITHOUT_GRID_NAME=COLOR_WITHOUT_GRID_NAME, save_path=save_path)


def save_image(image: ndarray, image_name: str, save_path: str):
    file_name = os.path.join(save_path, image_name)
    # file_name2 = os.path.join(save_path, image_name+'ski')
    # skimage.io.imsave(fname=file_name, arr=image)
    # image = convert_from_rgb_to_bgr(image)
    cv2.imwrite(filename=file_name, img=image)


def convert_to_mask(image: ndarray) -> ndarray:
    _image = convert_to_black_and_white(image=image)
    return cv2.bitwise_not(_image)
    # return skimage.util.invert(image)


def convert_to_black_and_white(image: ndarray) -> ndarray:
    _image = convert_to_grey_scale(image=image)
    (_, _image) = cv2.threshold(_image, 150, 255, cv2.THRESH_BINARY)
    return _image
    # thresh = skimage.filters.threshold_isodata(image)
    # return image > thresh


def convert_to_grey_scale(image: ndarray) -> ndarray:
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # return skimage.COLOR.rgb2gray(image)


def convert_to_bytes(image: ndarray) -> bytes:
    return cv2.imencode(DEFAULT_FILE_EXTENSION, image)[1].tobytes()


def convert_from_bytes(stream) -> ndarray:
    image = np.frombuffer(stream, dtype=np.uint8)  # <class 'numpy.ndarray'>
    # image = np.fromstring(stream, dtype=np.uint8)

    return cv2.imdecode(image, cv2.IMREAD_UNCHANGED)


def convert_to_base64_string(image: ndarray) -> str:
    image_array = cv2.imencode(DEFAULT_FILE_EXTENSION, image)[1]
    return base64.b64encode(image_array).decode()


def convert_from_base64_string(stream: str) -> ndarray:
    jpg_original = base64.b64decode(stream)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img

    # image = base64.b64decode(stream)
    # return convert_from_bytes(image)


# def create_binary_image(COLOR_WITHOUT_GRID_NAME: str, image_path: str) -> ndarray:
#     image = load_image(COLOR_WITHOUT_GRID_NAME=COLOR_WITHOUT_GRID_NAME, image_path=image_path, as_gray=True)
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
    return cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    # return skimage.COLOR.rgba2rgb(image)


def convert_from_brg_to_rgb(image: ndarray) -> ndarray:
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def convert_from_rgb_to_bgr(image: ndarray) -> ndarray:
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


#

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

# def add_salt_and_pepper_to_image(image: ndarray):
#     prob = 0.05
#     output = np.zeros(image.shape, np.uint8)
#     thres = 1 - prob
#     for i in range(image.shape[0]):
#         for j in range(image.shape[1]):
#             rdn = random.random()
#             if rdn < prob:
#                 output[i][j] = 0
#             elif rdn > thres:
#                 output[i][j] = 255
#             else:
#                 output[i][j] = image[i][j]
#     return output


def add_salt_and_pepper_to_image(image: ndarray, amount: float = 0.05, salt_vs_pepper: float = 0.5) -> ndarray:
    """
    Function to add random salt and pepper noise to a ndarray image.

    Original source https://gist.github.com/gutierrezps/f4ddad3bbd2ad5a9b96e3c06378e28b4
    Parameters
    ----------
    image: ndarray
        Input image data.
    amount: float, optional
        Proportion of image pixels to replace with noise on range [0, 1].
        Used in 'salt', 'pepper', and 'salt & pepper'. Default : 0.05
    salt_vs_pepper: float, optional
        Proportion of salt vs. pepper noise for 's&p' on range [0, 1].
        Higher values represent more salt. Default : 0.5 (equal amounts)

    Returns
    -------
    out : ndarray
        Output floating-point image data on range [0, 1] or [-1, 1] if the
        input `image` was unsigned or signed, respectively.
    """
    if 1.0 < salt_vs_pepper < 0.0:
        raise ValueError("salt_vs_pepper value needs to be equal or between 0.0 - 1.0")

    out = image.copy()
    if len(image.shape) == 2:
        black = 0
        white = 255
    else:
        colorspace = image.shape[2]
        if colorspace == 3:  # RGB
            black = np.array([0, 0, 0], dtype="uint8")
            white = np.array([255, 255, 255], dtype="uint8")
        else:  # RGBA
            black = np.array([0, 0, 0, 255], dtype="uint8")
            white = np.array([255, 255, 255, 255], dtype="uint8")
    probs = np.random.random(out.shape[:2])

    pepper_vs_salt = 1.0 - salt_vs_pepper

    out[probs < (amount * pepper_vs_salt)] = black
    out[probs > 1 - (amount * salt_vs_pepper)] = white
    return out

    # return sp_noise(image=image, amount=0.1)


#     # Getting the dimensions of the image
#     row, col, _ = image.shape
#     number_of_pixels = int((row * col) * 0.5)
#     # Randomly pick some pixels in the
#     # image for coloring them white
#     # Pick a random number between 300 and 10000
#     # number_of_pixels = random.randint(90000, 100000)
#     for i in range(number_of_pixels):
#         # Pick a random y coordinate
#         y_coord = random.randint(0, row - 1)
#
#         # Pick a random x coordinate
#         x_coord = random.randint(0, col - 1)
#
#         # Color that pixel to white
#         image[y_coord][x_coord] = 255
#
#     # Randomly pick some pixels in
#     # the image for coloring them black
#     # Pick a random number between 300 and 10000
#     number_of_pixels = random.randint(300, 10000)
#     for i in range(number_of_pixels):
#         # Pick a random y coordinate
#         y_coord = random.randint(0, row - 1)
#
#         # Pick a random x coordinate
#         x_coord = random.randint(0, col - 1)
#
#         # Color that pixel to black
#         image[y_coord][x_coord] = 0
#
#     return image


def add_salt_to_image(image: ndarray, amount: float = 0.05) -> ndarray:
    """
    Function to add random salt noise to a ndarray image.

    Original source https://gist.github.com/gutierrezps/f4ddad3bbd2ad5a9b96e3c06378e28b4
    Parameters
    ----------
    image: ndarray
        Input image data.
    amount: float, optional
        Proportion of image pixels to replace with noise on range [0, 1].
        Used in 'salt', 'pepper', and 'salt & pepper'. Default : 0.05

    Returns
    -------
    out : ndarray
        Output floating-point image data on range [0, 1] or [-1, 1] if the
        input `image` was unsigned or signed, respectively.
    """
    return add_salt_and_pepper_to_image(image=image, amount=amount, salt_vs_pepper=1.0)


def add_pepper_to_image(image: ndarray, amount: float = 0.05) -> ndarray:
    """
    Function to add random pepper noise to a ndarray image.

    Original source https://gist.github.com/gutierrezps/f4ddad3bbd2ad5a9b96e3c06378e28b4
    Parameters
    ----------
    image: ndarray
        Input image data.
    amount: float, optional
        Proportion of image pixels to replace with noise on range [0, 1].
        Used in 'salt', 'pepper', and 'salt & pepper'. Default : 0.05

    Returns
    -------
    out : ndarray
        Output floating-point image data on range [0, 1] or [-1, 1] if the
        input `image` was unsigned or signed, respectively.
    """
    return add_salt_and_pepper_to_image(image=image, amount=amount, salt_vs_pepper=0.0)
