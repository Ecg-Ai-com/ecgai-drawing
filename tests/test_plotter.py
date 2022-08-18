import os

import pytest
from fluentcheck import Is
from numpy import ndarray

from ecgai_drawing.ecg_plotter import EcgPlotter
from ecgai_drawing.enums.color_style import ColorStyle
from ecgai_drawing.enums.show_grid import ShowGrid
from ecgai_drawing.images import save_image

# noinspection DuplicatedCode
from tests.test_helper import setup_test_record_data, single_valid_record_path_name

# from tests.helper import setup_test_record_data, single_valid_record_path_name


class TestEcgPlot:
    # @pytest.fixture
    # @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
    # def ecg_plotter(self, record_path_name):
    #     record = setup_test_record_data(path_name=record_path_name)
    #     # leads = create_signal_list(record.leads)
    #     ecg_plotter = EcgPlotter()
    #     return ecg_plotter

    @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
    def test_create_ecg_plotter_and_convert_ecg_leads_to_ndarray(
        self, record_path_name
    ):
        record = setup_test_record_data(path_name=record_path_name)
        ecg_plotter = EcgPlotter()
        sut = ecg_plotter._convert_to_ndarray(record)
        assert type(sut) is ndarray
        assert len(sut) == 12

    @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
    def test_create_ecg_plot_save_as_colour_png_with_grid_default(
        self, record_path_name, tmp_path
    ):
        # Arrange
        print(tmp_path)
        record = setup_test_record_data(path_name=record_path_name)
        ecg_plotter = EcgPlotter()
        # Act
        image = ecg_plotter.plot(sample_rate=record.sample_rate, ecg_leads=record)
        save_image(image=image, image_name="test.png", save_path=str(tmp_path))
        # await ecg_plotter.save(file_name='test', path=str(tmp_path), extension='.png')
        # Assert
        assert ecg_plotter.color_style == ColorStyle.color
        assert ecg_plotter.show_grid == ShowGrid.false
        number_of_files = len(os.listdir(tmp_path))
        Is(number_of_files).between(1, 1)

    @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
    def test_create_ecg_plot_save_as_colour_png_without_grid(
        self, record_path_name, tmp_path
    ):
        # Arrange
        record = setup_test_record_data(path_name=record_path_name)
        ecg_plotter = EcgPlotter()
        show_grid = ShowGrid.false
        # Act
        image = ecg_plotter.plot(
            sample_rate=record.sample_rate, ecg_leads=record, show_grid=show_grid
        )
        save_image(image=image, image_name="test.png", save_path=str(tmp_path))
        # Assert
        assert ecg_plotter.color_style == ColorStyle.color
        assert ecg_plotter.show_grid == show_grid
        number_of_files = len(os.listdir(tmp_path))
        Is(number_of_files).between(1, 1)

    @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
    def test_create_ecg_plot_save_as_black_and_white_png_with_grid(
        self, record_path_name, tmp_path
    ):
        # Arrange
        record = setup_test_record_data(path_name=record_path_name)
        ecg_plotter = EcgPlotter()
        color_style = ColorStyle.black_and_white
        # Act
        image = ecg_plotter.plot(
            sample_rate=record.sample_rate,
            ecg_leads=record,
            color_style=color_style,
            show_grid=ShowGrid.true,
        )
        save_image(image=image, image_name="test.png", save_path=str(tmp_path))
        # await ecg_plotter.save(file_name='test', path=str(tmp_path), extension='.png')
        # Assert
        assert ecg_plotter.color_style == color_style
        assert ecg_plotter.show_grid == ShowGrid.true
        number_of_files = len(os.listdir(tmp_path))
        Is(number_of_files).between(1, 1)

    @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
    def test_create_ecg_plot_save_as_black_and_white_png_without_grid(
        self, record_path_name, tmp_path
    ):
        # Arrange
        record = setup_test_record_data(path_name=record_path_name)
        ecg_plotter = EcgPlotter()
        color_style = ColorStyle.black_and_white
        show_grid = ShowGrid.false
        # Act
        image = ecg_plotter.plot(
            sample_rate=record.sample_rate,
            ecg_leads=record,
            color_style=color_style,
            show_grid=show_grid,
        )
        save_image(image=image, image_name="test.png", save_path=str(tmp_path))
        # Assert
        assert ecg_plotter.color_style == color_style
        assert ecg_plotter.show_grid == show_grid
        number_of_files = len(os.listdir(tmp_path))
        Is(number_of_files).between(1, 1)

    @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
    def test_create_ecg_plot_save_as_mask_png(self, record_path_name, tmp_path):
        # Arrange
        record = setup_test_record_data(path_name=record_path_name)
        ecg_plotter = EcgPlotter()
        color_style = ColorStyle.mask
        show_grid = ShowGrid.true
        # Act
        image = ecg_plotter.plot(
            sample_rate=record.sample_rate,
            ecg_leads=record,
            color_style=color_style,
            show_grid=show_grid,
        )
        save_image(image=image, image_name="test.png", save_path=str(tmp_path))
        # Assert
        assert ecg_plotter.color_style == color_style
        assert ecg_plotter.show_grid == ShowGrid.false
        number_of_files = len(os.listdir(tmp_path))
        Is(number_of_files).between(1, 1)

    # @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
    # def test_create_ecg_plot_save_as_binary_png(self, record_path_name, tmp_path):
    #     # Arrange
    #     record = setup_test_record_data(path_name=record_path_name)
    #     ecg_plotter = EcgPlotter()
    #     color_style = ColorStyle.binary
    #     show_grid = ShowGrid.true
    #     # Act
    #     image = ecg_plotter.plot(
    #         ecg_leads=record, color_style=color_style, show_grid=show_grid
    #     )
    #     save_image(image=image, image_name="test.png", save_path=str(tmp_path))
    #     # Assert
    #     assert ecg_plotter.color_style == color_style
    #     assert ecg_plotter.show_grid == ShowGrid.false
    #     number_of_files = len(os.listdir(tmp_path))
    #     Is(number_of_files).between(1, 1)

    # @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
    #
    # async def test_create_ecg_plot_save_as_png_style_black_line(self, ecg_plotter,
    # tmp_path): # Arrange ecg_plotter.style = 'bl' # Act ecg_plotter.plot() await
    # ecg_plotter.save(file_name='test', path=str(tmp_path), extension='.png') #
    # Assert number_of_files = len(os.listdir(tmp_path)) Is(number_of_files).between(
    # 1, 1)
    #
    # @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
    # async def test_create_ecg_plot_save_as_png_style_black_and_thick_line(self,
    # ecg_plotter, tmp_path): # Arrange ecg_plotter.style = 'bl'
    # ecg_plotter.line_width = 1 # Act ecg_plotter.plot() await ecg_plotter.save(
    # file_name='test', path=str(tmp_path), extension='.png') # Assert
    # number_of_files = len(os.listdir(tmp_path)) Is(number_of_files).between(1, 1)
    #
    # @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
    # async def test_create_ecg_plot_save_as_png_style_thin_and_thin_line(self,
    # ecg_plotter, tmp_path): # Arrange ecg_plotter.style = 'tl'
    # ecg_plotter.line_width = 0.3 # Act ecg_plotter.plot() await ecg_plotter.save(
    # file_name='test', path=str(tmp_path), extension='.png') # Assert
    # number_of_files = len(os.listdir(tmp_path)) Is(number_of_files).between(1, 1)
    #
    # @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
    # async def test_create_ecg_plot_save_as_png_style_thin_and_thick_line(self,
    # ecg_plotter, tmp_path): # Arrange ecg_plotter.style = 'tl'
    # ecg_plotter.line_width = 0.8 # Act ecg_plotter.plot() await ecg_plotter.save(
    # file_name='test', path=str(tmp_path), extension='.png') # Assert
    # number_of_files = len(os.listdir(tmp_path)) Is(number_of_files).between(1, 1)
    #
    # @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
    # async def test_create_ecg_plot_save_as_png_style_black_and_white(self,
    # ecg_plotter, tmp_path): # Arrange ecg_plotter.style = 'bw' # Act
    # ecg_plotter.plot() await ecg_plotter.save(file_name='test', path=str(tmp_path),
    # extension='.png') # Assert number_of_files = len(os.listdir(tmp_path)) Is(
    # number_of_files).between(1, 1) @pytest.mark.parametrize("record_path_name",
    # single_valid_record_path_name) @pytest.mark.asyncio
    # def test_create_ecg_plot_save_as_svg(self, record_path_name, tmp_path): #
    # Arrange record = setup_test_record_data(path_name=record_path_name) leads =
    # create_signal_list(record.leads) # Act ecg_plotter = EcgPlotter(ecg=leads)
    # ecg_plotter.plot() ecg_plotter.save(file_name='test', path=tmp_path,
    # extension='svg') # Assert number_of_files = len(os.listdir(tmp_path)) Is(
    # number_of_files).between(1, 1)

    # @pytest.mark.parametrize("record_path_name", single_valid_record_path_name)
    # async def test_create_ecg_plot_save_tiff(self, record_path_name, tmp_path):
    #     # Arrange
    #     record = setup_test_record_data(path_name=record_path_name)
    #     leads = create_signal_list(record.leads)
    #     # Act
    #     ecg_plotter = EcgPlotter(ecg=leads)
    #     # ecg_plotter.plot()
    #     ecg_plotter.save(file_name='test', path=str(tmp_path), extension='.tiff')
    #     # Assert
    #     number_of_files = len(os.listdir(tmp_path))
    #     Is(number_of_files).between(1, 1)
