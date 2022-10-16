from math import ceil

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Subplot
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator
from numpy import ndarray
from pydantic.dataclasses import dataclass

from ecgai_drawing import images
from ecgai_drawing.enums.color_style import ColorStyle
from ecgai_drawing.models.ecg_leads import Leads

# from skimage.COLOR import rgba2rgb


@dataclass
class EcgPlotter:
    class Config:
        use_enum_values = True

    lead_index_order = [
        "I",
        "II",
        "III",
        "aVR",
        "aVL",
        "aVF",
        "V1",
        "V2",
        "V3",
        "V4",
        "V5",
        "V6",
    ]
    lead_order: list = None
    sample_rate: int = 500
    title: str = "ECG 12 lead"
    color_style: ColorStyle = ColorStyle.COLOR
    line_width: float = 0.5
    columns: int = 2
    row_height: int = 6
    show_lead_name: bool = True
    show_grid: bool = False
    show_separate_line: bool = True
    adjust_subplots: bool = True

    def plot(
        self,
        sample_rate: int,
        ecg_leads: Leads,
        title: str = "ECG 12 lead",
        color_style: ColorStyle = ColorStyle.COLOR,
        show_grid: bool = False,
    ) -> ndarray:
        """

        Args:
            title: Title shown at the top of the ECG printout
            sample_rate: Number of signal samples per second
            ecg_leads: Leads collection for drawing onto ECG plot
            color_style: Color style of output, default is COLOR.
            Other options are black and white, MASK and binary format
            show_grid: Show ECG grids on plot

        Returns:
            ndarray:

        """
        self.sample_rate = sample_rate
        self.title = title
        self._set_style(color_style, show_grid)
        image = self._create_plot(ecg_leads)

        # convert from rgba format to rgb format
        image = images.convert_from_rgba_to_rgb(image=image)

        # convert from rgb format to bgr format required by openCv
        image = images.convert_from_rgb_to_bgr(image=image)

        return image

    def _draw_plot(self, ecg_leads: Leads):
        leads = self._convert_to_ndarray(ecg_leads=ecg_leads)

        if not self.lead_order:
            self.lead_order = list(range(len(leads)))

        length_seconds = len(leads[0]) / self.sample_rate
        number_of_leads = len(self.lead_order)
        rows = int(ceil(number_of_leads / self.columns))
        # display_factor = 2.5
        display_factor = 1
        # line_width = 0.5

        figure = self._setup_figure(display_factor, rows, length_seconds)

        x_max, x_min, y_max, y_min = self._set_xy_axis_size(length_seconds, rows)

        subplot = self._setup_subplot(figure, x_max, x_min, y_max, y_min)

        display_factor **= 0.5

        color_line, color_major_grid, color_minor_grid = self._set_line_style()

        if self.show_grid:
            self._draw_grid(
                subplot=subplot,
                color_major_grid=color_major_grid,
                color_minor_grid=color_minor_grid,
                display_factor=display_factor,
                x_max=x_max,
                x_min=x_min,
                y_max=y_max,
                y_min=y_min,
            )

        self._draw_plot_leads(
            subplot=subplot,
            color_line=color_line,
            display_factor=display_factor,
            leads=leads,
            length_seconds=length_seconds,
            number_of_leads=number_of_leads,
            rows=rows,
        )

    def _draw_plot_leads(
        self,
        subplot: Subplot,
        color_line: tuple[float, float, float],
        display_factor: float,
        leads: ndarray,
        length_seconds: float,
        number_of_leads: int,
        rows: int,
    ):
        for column in range(self.columns):
            for row in range(rows):
                if column * rows + row < number_of_leads:
                    y_offset = -(self.row_height / 2) * ceil(row % rows)
                    # if y_offset < -5:
                    #     y_offset = y_offset + 0.25

                    x_offset = 0
                    if column > 0:
                        x_offset = length_seconds * column
                        if self.show_separate_line:
                            subplot.plot(
                                [x_offset, x_offset],
                                [
                                    leads[t_lead][0] + y_offset - 0.3,  # noqa
                                    leads[t_lead][0] + y_offset + 0.3,  # noqa
                                ],
                                linewidth=self.line_width * display_factor,
                                color=color_line,
                            )

                    t_lead = self.lead_order[column * rows + row]

                    step = 1.0 / self.sample_rate
                    if self.show_lead_name:
                        subplot.text(
                            x_offset + 0.07,
                            y_offset - 0.5,
                            self.lead_index_order[t_lead],
                            fontsize=9 * display_factor,
                        )
                    subplot.plot(
                        np.arange(0, len(leads[t_lead]) * step, step) + x_offset,
                        leads[t_lead] + y_offset,
                        linewidth=self.line_width * display_factor,
                        color=color_line,
                    )

    def _set_xy_axis_size(self, length_seconds: float, rows: int) -> tuple[float, float, float, float]:
        x_min = 0
        x_max = self.columns * length_seconds
        y_min = self.row_height / 4 - (rows / 2) * self.row_height
        y_max = self.row_height / 4
        return x_max, x_min, y_max, y_min

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

    def _setup_figure(self, display_factor: float, rows: int, length_seconds: float) -> Figure:
        figure = plt.figure(
            figsize=(
                length_seconds * self.columns * display_factor,
                rows * self.row_height / 5 * display_factor,
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

        figure.suptitle(self.title)
        if self.adjust_subplots:
            figure.subplots_adjust(bottom=0.00001)
            figure.subplots_adjust(right=0.99999)
            # figure.subplots_adjust(left=0.00001)
            # figure.subplots_adjust(top=0.99999)
        return figure

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

        # if self.style == 'bw':
        #     color_major_grid = (0.4, 0.4, 0.4)
        #     color_minor_grid = (0.75, 0.75, 0.75)
        #     color_line = (0, 0, 0)
        # elif self.style == 'tl':
        #     color_major_grid = (0.8, 0.8, 0.8)
        #     color_minor_grid = (0.8, 0.8, 0.8)
        #     color_line = (0, 0, 0.3)
        # elif self.style == 'bl':
        #     color_major_grid = (1, 0, 0)
        #     color_minor_grid = (1, 0.7, 0.7)
        #     color_line = (0, 0, 0.1)
        # else:
        #     color_major_grid = (1, 0, 0)
        #     color_minor_grid = (1, 0.7, 0.7)
        #     color_line = (0, 0, 0.7)
        # return color_line, color_major_grid, color_minor_grid

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
        subplot.minorticks_on()
        subplot.xaxis.set_minor_locator(AutoMinorLocator(5))
        subplot.grid(
            which="major",
            linestyle="-",
            linewidth=0.5 * display_factor,
            color=color_major_grid,
        )
        subplot.grid(
            which="minor",
            linestyle="-",
            linewidth=0.5 * display_factor,
            color=color_minor_grid,
        )

    def _create_plot(self, ecg_leads):
        plt.ioff()
        self._draw_plot(ecg_leads=ecg_leads)
        canvas = plt.get_current_fig_manager().canvas
        plt.close()
        agg = canvas.switch_backends(FigureCanvasAgg)
        agg.draw()
        return np.asarray(agg.buffer_rgba())

    # @staticmethod
    # def _convert_to_mask(image: ndarray) -> ndarray:
    #     return images.convert_to_mask(image)

    def _set_style(self, color_style: ColorStyle, show_grid: bool):
        if show_grid != self.show_grid:
            self.show_grid = show_grid

        if color_style != self.color_style:
            self.color_style = color_style
            if self.color_style in [ColorStyle.MASK]:
                self._set_mask_style()

    def _set_mask_style(self):
        self.show_grid = False
        self.show_lead_name = False
        self.title = ""

    @staticmethod
    def _convert_to_ndarray(ecg_leads: Leads) -> ndarray:
        ecg_leads.leads.sort()
        number_of_leads = len(ecg_leads.leads)
        lead_signal = ecg_leads.leads[0].signal
        number_of_signals = len(lead_signal)
        output_array = np.zeros(shape=[number_of_leads, number_of_signals])
        for i, s in enumerate(ecg_leads.leads):
            p_lead = np.array(s.signal)
            output_array[i] = p_lead
        return output_array

    # convert for protobuf models
    # @staticmethod
    # def _convert_to_ndarray(ecg_leads: Leads) -> ndarray:
    #     ecg_leads.leads.sort()
    #     number_of_leads = len(ecg_leads.leads)
    #     lead_signal = ecg_leads.leads[0].signals
    #     number_of_signals = len(lead_signal)
    #     output_array = np.zeros(shape=[number_of_leads, number_of_signals])
    #     for array_position, lead in enumerate(ecg_leads.leads):
    #         sig = [v.voltage for v in lead.signals]
    #         # g = s.signals
    #         p_lead = np.array(sig)
    #         output_array[array_position] = p_lead
    #     return output_array
