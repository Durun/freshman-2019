from abc import ABCMeta, abstractmethod
from typing import List, Optional
import logging
import cv2
import numpy
import copy


class Image(metaclass=ABCMeta):  # abstract class
    """
    OpenCVで扱う, numpy配列で表現された画像を, ラップしたもの.

    SubClasses
    ----------
    ColorImage,
    GrayImage

    Fields
    ------
    data : numpy.ndarray
        画像を表すnumpy配列.
    """
    data: numpy.ndarray

    def copy(self):
        """
        自身を複製
        """
        raise NotImplementedError

    def toGray(self):
        """
        グレースケール画像へ変換
        """
        raise NotImplementedError

    def isNChannelCorrect(self) -> bool:
        raise NotImplementedError

    def __init__(self, img):
        self.data = img
        if not self.isNChannelCorrect():
            message = """
            画像のチャンネル数が異なるため初期化できません.
            nDim=%d (expected=%d)
            """ % (nDim, expectedNDim)
            raise AssertionError(message)
        logging.info("new Image %dch %dx%d" %
                     (self.nChannel(), self.data.shape[0], self.data.shape[1]))

    def nChannel(self) -> int:
        """
        チャンネル数を返す
        """
        shape = self.data.shape
        n = shape[2] if len(shape) == 3 else 1
        return n

    def show(self, windowName: str) -> None:
        """
        画像をウィンドウに表示

        Parameters
        ----------
        windowName: str
            ウィンドウ名(既に同名のウィンドウがある場合、そのウィンドウを更新)
        """
        cv2.imshow(windowName, self.data)

    def resize(self, scale):
        self.data = cv2.resize(self.data, None,
                               fx=scale, fy=scale,
                               interpolation=cv2.INTER_CUBIC)
        return self

    def _copy(self):
        logging.info("new copy-Image %dch %dx%d" %
                     (self.nChannel(), self.data.shape[0], self.data.shape[1]))
        return copy.deepcopy(self)

    def warp(self, homography: Optional[List[float]]):
        raise NotImplementedError

    def _warp(self, homography: Optional[List[float]], width: int, height: int):
        shape = (width, height)
        if homography is not None:
            self.data = cv2.warpPerspective(self.data, homography, shape)
        return self

    def rotate(self, degree: float):
        raise NotImplementedError

    def _rotate(self, degree: float):
        size = self.data.shape[0:2]
        height, width = size
        center = (height/2, width/2)
        matrix = cv2.getRotationMatrix2D(center, degree, scale=1.0)
        self.data = cv2.warpAffine(self.data,
                                   M=matrix,
                                   dsize=size,
                                   flags=cv2.INTER_CUBIC)
        return self
