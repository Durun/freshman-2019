from __future__ import annotations
from typing import List, Optional
import cv2
import numpy
import PIL.Image
from .image import Image


class GrayImage(Image):
    """
    グレースケール画像

    SuperClass
    ----------
    Image
    """

    def isNChannelCorrect(self) -> bool:
        return self.nChannel() == 1

    def copy(self) -> GrayImage:
        """
        自身の複製を返す
        """
        return super()._copy()

    def toGray(self) -> GrayImage:
        """
        グレースケール画像へ変換
        """
        return self

    def toPilImage(self) -> PIL.Image:
        """
        PIL.Image型へ変換
        """
        pilImage = PIL.Image.fromarray(self.data)
        return pilImage

    def resize(self, scale: float) -> GrayImage:
        """
        拡大・縮小

        Parameters
        ----------
        scale : float
            拡大率
        """
        return super().resize(scale)

    def warp(self, homography: Optional[List[float]]) -> GrayImage:
        height, width = self.data.shape
        return self._warp(homography, width=width, height=height)

    def rotate(self, degree: float) -> GrayImage:
        return self._rotate(degree)

    def binarize(self) -> GrayImage:
        """
        ２値化
        """
        self.data = cv2.adaptiveThreshold(
            src=self.data,
            maxValue=255,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY,
            blockSize=11,
            C=2
        )
        return self

    def morphology(self, method: int, kernelSize: int) -> GrayImage:
        """
        モルフォロジー変換
        see also
        --------
        http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
        """
        shape = tuple([kernelSize]) * 2  # type : Tuple[int, int]
        kernel = numpy.ones(shape,
                            dtype=numpy.uint8)
        self.data = cv2.morphologyEx(
            src=self.data,
            op=method,
            kernel=kernel
        )
        return self

    def morph_erode(self, kernelSize: int) -> GrayImage:
        return self.morphology(cv2.MORPH_ERODE, kernelSize)

    def morph_dilate(self, kernelSize: int) -> GrayImage:
        return self.morphology(cv2.MORPH_DILATE, kernelSize)

    def morph_open(self, kernelSize: int) -> GrayImage:
        return self.morphology(cv2.MORPH_OPEN, kernelSize)

    def morph_close(self, kernelSize: int) -> GrayImage:
        return self.morphology(cv2.MORPH_CLOSE, kernelSize)

    def blur_median(self, kernelSize: int) -> GrayImage:
        """
        中央値フィルタ
        kernelSizeは奇数とすること.
        see also
        --------
        http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_filtering/py_filtering.html#id6
        """

        assert (kernelSize % 2) == 1, """
        kernelSizeは奇数でなければなりません.(given= %d) """ % kernelSize

        self.data = cv2.medianBlur(self.data, kernelSize)
        return self

    def normalize_clahe(self, clipLimit: float = 2.0, gridSize: int = 8) -> GrayImage:
        """
        ヒストグラム平均化(CLAHE法)
        see also
        --------
        http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_histograms/py_histogram_equalization/py_histogram_equalization.html#clahe-contrast-limited-adaptive-histogram-equalization
        """
        tile = tuple([gridSize]) * 2  # type : Tuple[int, int]
        normalizer = cv2.createCLAHE(clipLimit=clipLimit,
                                     tileGridSize=tile)
        self.data = normalizer.apply(self.data)
        return self

    def denoise(self) -> GrayImage:
        """
        ノイズ除去
        """
        self.data = cv2.fastNlMeansDenoising(self.data, None, 10, 7, 21)
        return self
