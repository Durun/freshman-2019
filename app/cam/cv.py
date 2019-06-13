from abc import ABCMeta, abstractmethod
import cv2


class Image(metaclass=ABCMeta):  # abstract class
    @classmethod
    def nChannel(cls) -> int:
        raise NotImplementedError

    def __init__(self, img):
        nDim = img.ndim
        expectedNDim = type(self).nChannel()
        if nDim != expectedNDim:
            message = """
            画像のチャンネル数が異なるため初期化できません.
            img.ndim=%d (expected=%d)
            """ % (nDim, expectedNDim)
            raise AssertionError(message)
        self.img = img

    def show(self, windowName: str) -> None:
        cv2.imshow(windowName, self.img)


class GrayImage(Image):
    @classmethod
    def nChannel(cls) -> int:
        return 2


class ColorImage(Image):
    @classmethod
    def nChannel(cls) -> int:
        return 3

    def toGray(self) -> GrayImage:
        grayImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        return GrayImage(grayImg)
