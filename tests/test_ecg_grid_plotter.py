import os

from ecgai_drawing.ecg_grid_plotter import EcgGridPlotter
from ecgai_drawing.enums.color_style import ColorStyle
from ecgai_drawing.images import save_image


def test_sorted_ecg_lead_enum(tmp_path):
    ecg_grid_plotter = EcgGridPlotter()
    image = ecg_grid_plotter.plot(x_length=2048, y_length=768, color_style=ColorStyle.COLOR)
    save_image(image=image, image_name="test.png", save_path=str(tmp_path))
    number_of_files = len(os.listdir(tmp_path))
    assert number_of_files == 1
