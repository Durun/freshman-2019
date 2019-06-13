from __future__ import annotations
from abc import ABCMeta, abstractmethod
import cv2
import numpy


class Image(metaclass=ABCMeta):  # abstract class
    data: numpy.ndarray

    @classmethod
    def nChannel(cls) -> int:
        raise NotImplementedError

    def __init__(self, img):
        nDim = img.ndim
        expectedNDim = type(self).nChannel()
        if nDim != expectedNDim:
            message = """
            画像のチャンネル数が異なるため初期化できません.
            nDim=%d (expected=%d)
            """ % (nDim, expectedNDim)
            raise AssertionError(message)
        self.data = img

    def show(self, windowName: str) -> None:
        cv2.imshow(windowName, self.data)

    def resize(self, scale):
        self.data = cv2.resize(self.data, None,
                               fx=scale, fy=scale,
                               interpolation=cv2.INTER_CUBIC)
        return self


class GrayImage(Image):
    @classmethod
    def nChannel(cls) -> int:
        return 2

    def resize(self, scale) -> GrayImage:
        return super().resize(scale)

    def binarize(self) -> GrayImage:
        binImg = cv2.adaptiveThreshold(
            src=self.data,
            maxValue=255,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY,
            blockSize=11,
            C=2)
        return binImg


class ColorImage(Image):
    @classmethod
    def nChannel(cls) -> int:
        return 3

    def resize(self, scale) -> ColorImage:
        return super().resize(scale)

    def toGray(self) -> GrayImage:
        grayImg = cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY)
        return GrayImage(grayImg)
