from abc import ABCMeta, abstractmethod
from typing import IO, Any
import cv2
import os
import tempfile
import io
import requests
from requests import ConnectionError
import logging
from .color_image import ColorImage


class ImageReadError(Exception):
    "画像読み込み失敗時エラー"


class ImageReader(metaclass=ABCMeta):  # abstract class
    """
    ColorImageをreadするもの.

    SubClasses
    ----------
    FileImageReader
    CameraImageReader
    """

    def read(self):
        raise NotImplementedError


class FileImageReader(ImageReader):
    """
    ファイルからColorImageをreadするもの.
    """

    def __init__(self, filePath: str):
        assert os.path.isfile(filePath), "ファイル "+filePath+" は存在しません"
        self.filePath = filePath

    def read(self):
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

    def __init__(self, url: str):
        self.url = url
        self.file = self.__createEmptyFile()

    @staticmethod
    def __createEmptyFile(suffix=""):
        dirPath = tempfile.gettempdir() + os.path.sep + "freshman2019-camera"
        os.makedirs(dirPath, exist_ok=True)
        newFile = tempfile.NamedTemporaryFile(
            mode="w+b", dir=dirPath, suffix=suffix)
        logging.info("Created tempfile : " + newFile.name)
        return newFile

    @staticmethod
    def __getSuffix(response: requests.Response):
        urlPath = response.request.path_url
        _, suffix = os.path.splitext(urlPath)
        return suffix

    def __updateFile(self):
        try:
            response = requests.get(self.url)
        except ConnectionError as err:
            logging.warn("failed to download from URL: " + self.url)
            raise err
        logging.info("Downloaded : " + self.url)
        suffix = self.__getSuffix(response)
        newFile = self.__createEmptyFile(suffix=suffix)
        newFile.write(response.content)
        self.file = newFile  # update
        return

    def __getFileReader(self):
        return FileImageReader(self.file.name)

    def read(self):
        self.__updateFile()
        reader = self.__getFileReader()
        return reader.read()


class CameraImageReader(ImageReader):
    """
    カメラデバイスからColorImageをreadするもの.
    """

    bufferSize = 1

    def __init__(self, deviceNumber: int):
        self.capture = cv2.VideoCapture(deviceNumber)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, self.__class__.bufferSize)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        logging.info("Initialized camera %d" % deviceNumber)

    def flush(self):
        n = self.__class__.bufferSize
        for i in range(n):
            self.capture.read()
        return

    def read(self):
        self.flush()
        ret, frame = self.capture.read()
        if ret == False:
            raise ImageReadError("can't read image from" + str(self.capture))
        return ColorImage(frame)
