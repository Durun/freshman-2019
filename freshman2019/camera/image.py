from abc import ABCMeta, abstractmethod
import cv2
import numpy


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

    @classmethod
    def nChannel(cls) -> int:
        raise NotImplementedError

    def toGray(self):
        """
        グレースケール画像へ変換
        """
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
