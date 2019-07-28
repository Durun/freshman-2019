
from typing import List, Optional
import cv2
import PIL.Image
from .image import Image
from .gray_image import GrayImage


class ColorImage(Image):
    """
    カラー画像

    SuperClass
    ----------
    Image
    """

    def isNChannelCorrect(self) -> bool:
        return self.nChannel() == 3

    def resize(self, scale: float) -> ColorImage:
        """
        拡大・縮小

        Parameters
        ----------
        scale : float
            拡大率
        """
        return super().resize(scale)

    def copy(self) -> ColorImage:
        """
        自身の複製を返す
        """
        return super()._copy()

    def toGray(self) -> GrayImage:
        """
        グレースケール画像へ変換
        """
        grayImg = cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY)
        return GrayImage(grayImg)

    def toPilImage(self) -> PIL.Image:
        """
        PIL.Image型へ変換
        """
        buffer = self.data.copy()
        buffer = cv2.cvtColor(buffer, cv2.COLOR_BGR2RGB)
        pilImage = PIL.Image.fromarray(buffer)
        return pilImage

    def warp(self, homography: Optional[List[float]]) -> ColorImage:
        height, width, _ = self.data.shape
        return self._warp(homography, width=width, height=height)

    def rotate(self, degree: float) -> ColorImage:
        return self._rotate(degree)
