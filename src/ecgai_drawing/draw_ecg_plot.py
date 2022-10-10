from numpy import ndarray

from ecgai_drawing import images
from ecgai_drawing.ecg_plot_request import EcgPlotRequest
from ecgai_drawing.ecg_plot_response import EcgPlotResponse
from ecgai_drawing.ecg_plotter import EcgPlotter
from ecgai_drawing.enums.artifact import Artifact
from ecgai_drawing.enums.color_style import ColorStyle
from ecgai_drawing.images import DEFAULT_FILE_EXTENSION, convert_to_bytes


class DrawEcgPlot:
    _plot_request: EcgPlotRequest

    # def __init__(self, plot_parameters: EcgPlotRequest):
    # self._plot_request = plot_parameters

    # self.transaction_id = transaction_id
    # self.record_name = record_name
    # self.color_style = color_style
    # self.artifact = artifact
    # self.show_grid = show_grid

    # ecg = 6;

    def handle(self, plot_request: EcgPlotRequest) -> EcgPlotResponse:
        self._plot_request = plot_request
        image = self._create_image()
        return EcgPlotResponse.create(
            transaction_id=self._plot_request.transaction_id,
            record_name=self._plot_request.record_name,
            file_name=self._plot_request.file_name,
            file_extension=DEFAULT_FILE_EXTENSION,
            image=convert_to_bytes(image=image),
        )
        # return EcgPlotResponse(
        #     transaction_id=self._plot_request.transaction_id,
        #     record_name=self._plot_request.record_name,
        #     file_name=self._plot_request.file_name,
        #     image=convert_to_bytes(image=image),
        # )
        # return draw_response

    # def _create_response(self, image: ndarray) -> EcgPlotRequest:
    #     f, buffer = cv2.imencode(ext='.png', img=image)
    #     image_string = base64.b64encode(buffer)
    #     return EcgPlotRequest(
    #         transaction_id=self.transaction_id,
    #         record_name=self.ecg.record_name,
    #         file_name=self.file_name,
    #         image=image_string,
    #     )
    # return DrawEcgPlotResponseOld.create(transaction_id=self.transaction_id,
    # record_name=self.record_name, file_name="", image=image)

    def _create_image(self) -> ndarray:
        ecg_plotter = EcgPlotter()
        image = ecg_plotter.plot(
            sample_rate=self._plot_request.sample_rate,
            ecg_leads=self._plot_request.ecg_leads,
            title=self._plot_request.record_name,
            color_style=self._plot_request.color_style,
            show_grid=self._plot_request.show_grid,
        )
        image = self._add_artifact_to_image(image)
        image = self._convert_format(image)
        return image

    def _convert_format(self, image):

        if self._plot_request.color_style in [ColorStyle.color]:
            return image

        if self._plot_request.color_style == ColorStyle.black_and_white:
            image = images.convert_to_black_and_white(image=image)
            self._plot_request.file_name = f"bw_{self._plot_request.file_name}"
        elif self._plot_request.color_style == ColorStyle.grey_scale:
            image = images.convert_to_grey_scale(image=image)
            self._plot_request.file_name = f"gs_{self._plot_request.file_name}"
        elif self._plot_request.color_style == ColorStyle.mask:
            image = images.convert_to_mask(image=image)
            self._plot_request.file_name = f"mask_{self._plot_request.file_name}"

            #
            # if self.color_style in [
            #     ColorStyle.mask,
            # ]:
            #     # image = self.convert_to_binary(image=image)
            #     image = self.convert_to_mask(image=image)

        return image

    def _add_artifact_to_image(self, image):

        if (
            self._plot_request.color_style != ColorStyle.mask
            and self._plot_request.artifact != Artifact.artifact_unspecified
        ):

            if self._plot_request.artifact == Artifact.pepper:
                image = images.add_pepper_to_image(image=image)
                self._plot_request.file_name = f"p_{self._plot_request.file_name}"
            elif self._plot_request.artifact == Artifact.salt:
                image = images.add_salt_to_image(image=image)
                self._plot_request.file_name = f"s_{self._plot_request.file_name}"
            elif self._plot_request.artifact == Artifact.salt_and_pepper:
                image = images.add_salt_and_pepper_to_image(image=image)
                self._plot_request.file_name = f"sp_{self._plot_request.file_name}"
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
