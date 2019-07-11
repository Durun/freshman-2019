from abc import ABCMeta, abstractmethod
from typing import IO, Any
import cv2
import os
import tempfile
import io
import requests
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


class UrlImageReader(ImageReader):
    """
    URLからColorImageをreadするもの.

    Fields
    ------
    file: IO[Any]
        画像を保存する一時ファイル.
        インスタンス終了時に自動で削除されます.
    """
    url: str
    file: IO[Any]

    def __init__(self, url: str):
        self.url = url
        self.file = self.__createEmptyFile()

    @staticmethod
    def __createEmptyFile(suffix="") -> IO[Any]:
        return tempfile.NamedTemporaryFile(mode="w+b", suffix=suffix)

    @staticmethod
    def __getSuffix(response: requests.Response) -> str:
        urlPath = response.request.path_url
        _, suffix = os.path.splitext(urlPath)
        return suffix

    def __updateFile(self) -> None:
        response = requests.get(self.url)
        suffix = self.__getSuffix(response)
        newFile = self.__createEmptyFile(suffix=suffix)
        newFile.write(response.content)
        self.file = newFile  # update
        return

    def __getFileReader(self) -> FileImageReader:
        return FileImageReader(self.file.name)

    def read(self) -> ColorImage:
        self.__updateFile()
        reader = self.__getFileReader()
        return reader.read()


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
