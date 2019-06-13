from __future__ import annotations
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


class GrayImage(Image):
    """
    グレースケール画像

    SuperClass
    ----------
    Image
    """
    @classmethod
    def nChannel(cls) -> int:
        return 2

    def resize(self, scale: float) -> GrayImage:
        """
        拡大・縮小

        Parameters
        ----------
        scale : float
            拡大率
        """
        return super().resize(scale)

    def binarize(self) -> GrayImage:
        """
        ２値化
        """
        binImg = cv2.adaptiveThreshold(
            src=self.data,
            maxValue=255,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY,
            blockSize=11,
            C=2
        )
        return binImg

    def morphology(self, method: int, kernelSize: int) -> GrayImage:
        """
        モルフォロジー変換
        see also
        --------
        http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
        """
        shape = (kernelSize) * 2
        kernel = numpy.ones(shape,
                            dtype=numpy.uint8)
        img = cv2.morphologyEx(
            src=self.data,
            op=method,
            kernel=kernel
        )
        return img

    def morph_erode(self, kernelSize: int) -> GrayImage:
        return self.morphology(cv2.MORPH_ERODE, kernelSize)

    def morph_dilate(self, kernelSize: int) -> GrayImage:
        return self.morphology(cv2.MORPH_DILATE, kernelSize)

    def morph_open(self, kernelSize: int) -> GrayImage:
        return self.morphology(cv2.MORPH_OPEN, kernelSize)

    def morph_close(self, kernelSize: int) -> GrayImage:
        return self.morphology(cv2.MORPH_CLOSE, kernelSize)


class ColorImage(Image):
    """
    カラー画像

    SuperClass
    ----------
    Image
    """

    @classmethod
    def nChannel(cls) -> int:
        return 3

    def resize(self, scale: float) -> ColorImage:
        """
        拡大・縮小

        Parameters
        ----------
        scale : float
            拡大率
        """
        return super().resize(scale)

    def toGray(self) -> GrayImage:
        """
        グレースケール画像へ変換
        """
        grayImg = cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY)
        return GrayImage(grayImg)
