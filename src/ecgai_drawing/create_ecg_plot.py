from numpy import ndarray

from ecgai_drawing import images
from ecgai_drawing.ecg_plot_image import EcgPlotImage
from ecgai_drawing.ecg_plotter import EcgPlotter
from ecgai_drawing.enums.artifact import Artifact
from ecgai_drawing.enums.color_style import ColorStyle
from ecgai_drawing.images import (
    DEFAULT_FILE_EXTENSION,
    convert_from_rgba_to_rgb,
    convert_to_bytes,
)
from ecgai_drawing.models.ecg_leads import Leads


class CreateEcgPlot:
    # _plot_request: EcgPlotRequest
    transaction_id: str
    record_name: str
    sample_rate: int
    color_style: ColorStyle
    show_grid: bool
    artifact: Artifact
    ecg_leads: Leads
    file_name: str

    def __init__(
        self,
        transaction_id: str,
        record_name: str,
        sample_rate: int,
        ecg_leads: Leads,
        file_name: str = "",
        color_style: ColorStyle = ColorStyle.BLACK_AND_WHITE,
        show_grid: bool = True,
        artifact: Artifact = Artifact.NONE,
    ):
        self.transaction_id = transaction_id
        self.record_name = record_name
        self.sample_rate = sample_rate
        self.ecg_leads = ecg_leads
        if file_name == "":
            self.file_name = record_name
        else:
            self.file_name = file_name
        self.color_style = color_style
        self.artifact = artifact
        self.show_grid = show_grid

    # ecg = 6;

    def handle(self) -> EcgPlotImage:
        image = self._create_image()
        return EcgPlotImage.create(
            transaction_id=self.transaction_id,
            record_name=self.record_name,
            file_name=self.file_name,
            file_extension=DEFAULT_FILE_EXTENSION,
            image=convert_to_bytes(image=image),
        )
        # return EcgPlotImage(
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
            sample_rate=self.sample_rate,
            ecg_leads=self.ecg_leads,
            title=self.record_name,
            color_style=self.color_style,
            show_grid=self.show_grid,
        )
        image = convert_from_rgba_to_rgb(image)
        image = self._add_artifact_to_image(image)
        image = self._convert_format(image)
        self._is_grid_name()
        return image

    def _is_grid_name(self):
        if self.color_style != ColorStyle.MASK:
            if not self.show_grid:
                self.file_name = f"ng_{self.file_name}"

    def _convert_format(self, image):

        if self.color_style in [ColorStyle.COLOR]:
            return image

        if self.color_style == ColorStyle.BLACK_AND_WHITE:
            image = images.convert_to_black_and_white(image=image)
            self.file_name = f"bw_{self.file_name}"
        elif self.color_style == ColorStyle.GREY_SCALE:
            image = images.convert_to_grey_scale(image=image)
            self.file_name = f"gs_{self.file_name}"
        elif self.color_style == ColorStyle.MASK:
            image = images.convert_to_mask(image=image)
            self.file_name = f"mask_{self.file_name}"

            #
            # if self.color_style in [
            #     ColorStyle.MASK,
            # ]:
            #     # image = self.convert_to_binary(image=image)
            #     image = self.convert_to_mask(image=image)

        return image

    def _add_artifact_to_image(self, image):

        if (
            self.color_style != ColorStyle.MASK
            or self.artifact != Artifact.ARTIFACT_UNSPECIFIED
            or self.artifact != Artifact.NONE
        ):

            if self.artifact == Artifact.PEPPER:
                image = images.add_pepper_to_image(image=image)
                self.file_name = f"p_{self.file_name}"
            elif self.artifact == Artifact.SALT:
                image = images.add_salt_to_image(image=image)
                self.file_name = f"s_{self.file_name}"
            elif self.artifact == Artifact.SALT_AND_PEPPER:
                image = images.add_salt_and_pepper_to_image(image=image)
                self.file_name = f"sp_{self.file_name}"
            # else:
            #     raise ValueError()
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
