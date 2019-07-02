from abc import ABCMeta, abstractmethod
import cv2
import os
import logging
from .color_image import ColorImage


class ImageReader(metaclass=ABCMeta):  # abstract class
    """
    ColorImageをreadするもの.

    SubClasses
    ----------
    FileImageReader
    CameraImageReader
    """

    def read(self) -> ColorImage:
        raise NotImplementedError


class FileImageReader(ImageReader):
    """
    ファイルからColorImageをreadするもの.
    """
    filePath: str

    def __init__(self, filePath: str):
        assert os.path.isfile(filePath), "ファイル "+filePath+" は存在しません"
        self.filePath = filePath

    def read(self) -> ColorImage:
        data = cv2.imread(self.filePath)
        logging.info("read %s" % self.filePath)
        return ColorImage(data)


class CameraImageReader(ImageReader):
    """
    カメラデバイスからColorImageをreadするもの.
    """
    capture: cv2.VideoCapture

    def __init__(self, deviceNumber: int):
        self.capture = cv2.VideoCapture(deviceNumber)
        logging.info("Initialized camera %d" % deviceNumber)

    def read(self) -> ColorImage:
        ret, frame = self.capture.read()
        return ColorImage(frame)
