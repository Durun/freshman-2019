from __future__ import annotations
import cv2
from .image import Image
from .gray_image import GrayImage


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
