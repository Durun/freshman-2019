from .image import Image
from .feature import Feature
from .matcher import Matcher


class Detector(object):
    """
    特徴点抽出器
    """

    def __init__(self, detector):
        self.detector = detector

    def detect(self, image: Image) -> Feature:
        kp, des = self.detector.detectAndCompute(image.data, None)
        return Feature(image, kp, des)
