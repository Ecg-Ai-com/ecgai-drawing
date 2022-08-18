from numpy import ndarray

from ecgai_drawing import images
from ecgai_drawing.ecg_plot_response import DrawEcgPlotResponse
from ecgai_drawing.ecg_plotter import EcgPlotter
from ecgai_drawing.enums.artifact import Artifact
from ecgai_drawing.enums.color_style import ColorStyle


class DrawEcgPlot:
    _plot_parameters: DrawEcgPlotResponse

    def __init__(self, plot_parameters: DrawEcgPlotResponse):
        self._plot_parameters = plot_parameters

    # self.transaction_id = transaction_id
    # self.record_name = record_name
    # self.color_style = color_style
    # self.artifact = artifact
    # self.show_grid = show_grid

    # ecg = 6;
    def handle(self) -> ndarray:
        ecg_plotter = EcgPlotter()

        return self._create_image(ecg_plotter)
        # return self._create_response(image)

    # def _create_response(self, image: ndarray) -> DrawEcgPlotResponse:
    #     f, buffer = cv2.imencode(ext='.png', img=image)
    #     image_string = base64.b64encode(buffer)
    #     return DrawEcgPlotResponse(
    #         transaction_id=self.transaction_id,
    #         record_name=self.ecg.record_name,
    #         file_name=self.file_name,
    #         image=image_string,
    #     )
    # return DrawEcgPlotResponseOld.create(transaction_id=self.transaction_id,
    # record_name=self.record_name, file_name="", image=image)

    def _create_image(self, ecg_plotter) -> ndarray:
        image = ecg_plotter.plot(
            sample_rate=self._plot_parameters.sample_rate,
            ecg_leads=self._plot_parameters.ecg_leads,
            title=self._plot_parameters.record_name,
            color_style=self._plot_parameters.color_style,
            show_grid=self._plot_parameters.show_grid,
        )
        image = self._add_artifact_to_image(image)
        image = self._convert_format(image)
        return image

    def _convert_format(self, image):

        if self._plot_parameters.color_style == ColorStyle.black_and_white:
            image = images.convert_to_black_and_white(image=image)
            #
            # if self.color_style in [
            #     ColorStyle.mask,
            # ]:
            #     # image = self.convert_to_binary(image=image)
            #     image = self.convert_to_mask(image=image)

        return image

    def _add_artifact_to_image(self, image):

        if (
            self._plot_parameters.color_style != ColorStyle.mask
            and self._plot_parameters.artifact != Artifact.none
        ):

            if self._plot_parameters.artifact == Artifact.pepper:
                image = images.add_pepper_to_image(image=image)
            elif self._plot_parameters.artifact == Artifact.salt:
                image = images.add_salt_to_image(image=image)
            elif self._plot_parameters.artifact == Artifact.salt_and_pepper:
                image = images.add_salt_and_pepper_to_image(image=image)
            else:
                raise ValueError()
        return image

    # @staticmethod
    # def convert_to_mask(image: ndarray) -> ndarray:
    #     # return util.invert(image)
    #     return image

    # @staticmethod
    # def convert_to_binary(image: ndarray) -> ndarray:
    #     thresh = threshold_isodata(image)
    #     return image > thresh

    # @staticmethod
    # def add_salt_and_pepper_to_image(image: ndarray) -> ndarray:
    #     return skimage.util.random_noise(image=image, mode="s&p")
    #
    # @staticmethod
    # def add_salt_to_image(image: ndarray) -> ndarray:
    #     return skimage.util.random_noise(image=image, mode="salt")
    #
    # @staticmethod
    # def add_pepper_to_image(image: ndarray) -> ndarray:
    #     return skimage.util.random_noise(image=image, mode="pepper")
