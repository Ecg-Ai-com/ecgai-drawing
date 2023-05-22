from dataclasses import dataclass

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Subplot
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator

from ecgai_drawing import images
from ecgai_drawing.enums.color_style import ColorStyle


@dataclass
class EcgGridPlotter:
    def __init__(self):
        self.columns = 2
        self.adjust_subplots = True
        self.color_style = ColorStyle.BLACK_AND_WHITE
        self.line_width: float = 0.5
        self.row_height: int = 6
        self.display_factor = 1

    def plot(self, x_length, y_length, color_style):
        # length_seconds = 5000 / self.sample_rate
        # number_of_leads = len(self.lead_order)
        # rows = int(ceil(number_of_leads / self.columns))
        # display_factor = 2.5
        self.color_style = color_style
        # line_width = 0.5
        self._plot(x_length, y_length)

        canvas = plt.get_current_fig_manager().canvas

        plt.close()
        # agg=canvas
        agg = canvas.switch_backends(FigureCanvasAgg)

        agg.draw()
        image = np.asarray(agg.buffer_rgba())
        # convert from rgba format to rgb format
        image = images.convert_from_rgba_to_rgb(image=image)

        # convert from rgb format to bgr format required by openCv
        image = images.convert_from_rgb_to_bgr(image=image)

        return image

    def _plot(self, x_length, y_length):
        figure = self._setup_figure(x_height=x_length, y_length=y_length)
        x_max, x_min, y_max, y_min = self._set_xy_axis_size(10, 6)
        subplot = self._setup_subplot(figure, x_max, x_min, y_max, y_min)
        self.display_factor **= 0.5
        color_line, color_major_grid, color_minor_grid = self._set_line_style()
        self._draw_grid(
            subplot=subplot,
            color_major_grid=color_major_grid,
            color_minor_grid=color_minor_grid,
            display_factor=self.display_factor,
            x_max=x_max,
            x_min=x_min,
            y_max=y_max,
            y_min=y_min,
        )

    def _setup_figure(self, x_height: int, y_length: int) -> Figure:
        x_height = self.pixels_to_inches(x_height)
        y_length = self.pixels_to_inches(y_length)

        figure = plt.figure(
            figsize=(
                x_height,
                y_length,
            )
        )
        figure.subplots_adjust(
            hspace=0,
            wspace=0,
            left=0,  # the left side of the subplots of the figure
            right=1,  # the right side of the subplots of the figure
            bottom=0,  # the bottom of the subplots of the figure
            top=1,
        )

        if self.adjust_subplots:
            figure.subplots_adjust(bottom=0.00001)
            figure.subplots_adjust(right=0.99999)
            # figure.subplots_adjust(left=0.00001)
            # figure.subplots_adjust(top=0.99999)
        return figure

    @staticmethod
    def _draw_grid(
        subplot: Subplot,
        color_major_grid: tuple[float, float, float],
        color_minor_grid: tuple[float, float, float],
        display_factor: float,
        x_max: float,
        x_min: float,
        y_max: float,
        y_min: float,
    ):
        """

        Args:
            subplot:
            color_major_grid: Line COLOR for major grid lines
            color_minor_grid: Line COLOR for minor grid lines
            display_factor:
            x_max: X axis maximum position value
            x_min: X axis minimum position value
            y_max: Y axis maximum position value
            y_min: Y axis minimum position value

        Returns:

        """
        subplot.set_xticks(np.arange(x_min, x_max, 0.2))
        subplot.set_yticks(np.arange(y_min, y_max, 0.5))

        subplot.xaxis.set_minor_locator(AutoMinorLocator(5))

        subplot.grid(
            which="major",
            linestyle="-",
            linewidth=0.5 * display_factor,
            color=color_major_grid,
            zorder=2.5,
        )

        subplot.minorticks_on()

        subplot.grid(
            which="minor",
            linestyle="-",
            linewidth=0.5 * display_factor,
            color=color_minor_grid,
            zorder=0.5,
        )

    @staticmethod
    def _setup_subplot(figure, x_max: float, x_min: float, y_max: float, y_min: float) -> Subplot:
        subplot = figure.add_subplot(1, 1, 1)
        subplot.set_ylim(y_min, y_max)
        subplot.set_xlim(x_min, x_max)

        # remove black line box around plot
        subplot.spines["top"].set_visible(False)
        subplot.spines["right"].set_visible(False)
        subplot.spines["bottom"].set_visible(False)
        subplot.spines["left"].set_visible(False)
        return subplot

    def _set_xy_axis_size(self, length_seconds: float, rows: int) -> tuple[float, float, float, float]:
        x_min = 0
        x_max = self.columns * length_seconds
        y_min = self.row_height / 4 - (rows / 2) * self.row_height
        y_max = self.row_height / 4
        return x_max, x_min, y_max, y_min

    @staticmethod
    def pixels_to_inches(pixels: int, dpi: int = 100) -> float:
        inches = float(pixels / dpi)
        return inches

    def _set_line_style(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]:
        if self.color_style == ColorStyle.COLOR:
            color_major_grid = (1, 0, 0)
            color_minor_grid = (1, 0.7, 0.7)
            color_line = (0, 0, 0.7)
        elif self.color_style in [
            ColorStyle.BLACK_AND_WHITE,
            ColorStyle.GREY_SCALE,
            ColorStyle.MASK,
        ]:
            color_major_grid = (0.4, 0.4, 0.4)
            color_minor_grid = (0.75, 0.75, 0.75)
            color_line = (0, 0, 0)
        else:
            raise ValueError()

        return color_line, color_major_grid, color_minor_grid
