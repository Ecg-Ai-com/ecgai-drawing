import pydantic

from ecgai_drawing.models.model_base import MyBaseModel


class EcgPlotImage(MyBaseModel):
    transaction_id: str
    record_name: str
    file_name: str
    file_extension: str
    image: bytes

    # def __int__(
    #     self, transaction_id: str, record_name: str, file_name: str, image: bytes
    # ):
    #     self.transaction_id = transaction_id
    #     self.record_name = record_name
    #     self.file_name = file_name
    #     self.image = image

    @classmethod
    def create(cls, transaction_id: str, record_name: str, file_name: str, file_extension: str, image: bytes):
        try:
            d = dict(
                TransactionId=transaction_id,
                RecordName=record_name,
                FileName=file_name,
                FileExtension=file_extension,
                Image=image,
            )
            return cls.from_dict(d)
        except pydantic.ValidationError as e:
            # logging.error(e)
            raise e
