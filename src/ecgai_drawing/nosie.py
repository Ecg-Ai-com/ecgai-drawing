import numpy as np
from numpy import ndarray


def sp_noise(image: ndarray, amount: float = 0.05, salt_vs_pepper: float = 0.5) -> ndarray:
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
            white = np.array([125, 125, 125], dtype="uint8")
        else:  # RGBA
            black = np.array([0, 0, 0, 255], dtype="uint8")
            white = np.array([255, 255, 255, 255], dtype="uint8")
    probs = np.random.random(out.shape[:2])

    pepper_vs_salt = 1.0 - salt_vs_pepper

    out[probs < (amount * pepper_vs_salt)] = black
    out[probs > 1 - (amount * salt_vs_pepper)] = white
    return out
