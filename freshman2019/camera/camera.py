from .image_reader import ImageReader, UrlImageReader, CameraImageReader


class Camera(object):
    queryReader: ImageReader
    trainReader: ImageReader

    def __init__(self, deviceNumber: int, trainImageUrl: str):
        self.queryReader = CameraImageReader(deviceNumber)
        self.trainReader = UrlImageReader(trainImageUrl)

    def get_temperature(self) -> int:
        raise NotImplementedError

    def is_power_on(self) -> bool:
        raise NotImplementedError
