from .image_reader import ImageReader, FileImageReader, CameraImageReader


class Camera(object):
    queryReader: ImageReader
    trainReader: ImageReader

    def __init__(self, deviceNumber: int, trainImagePath: str):
        self.queryReader = CameraImageReader(deviceNumber)
        self.trainReader = FileImageReader(trainImagePath)

    def get_temperature(self) -> int:
        raise NotImplementedError

    def is_power_on(self) -> bool:
        raise NotImplementedError
