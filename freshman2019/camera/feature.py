from __future__ import annotations
import cv2
import numpy
import copy
from typing import List
from .image import Image


class Feature(object):
    """
    画像の特徴点

    Fields
    ------
    img: Image
        元の画像
    kp
        KeyPoint
    des
    """
    img: Image
    kp: List[cv2.KeyPoint]
    des: numpy.ndarray

    def __init__(self, img, kp, des):
        self.img = img
        self.kp = kp
        self.des = des

    def match(self, that: Feature, matcherAlgorithm: cv2.DescriptorMatcher) -> List[cv2.DMatch]:
        matches = matcherAlgorithm.match(self.des, that.des)
        return matches

    def plot(self) -> Image:
        newImg = copy.copy(self.img)
        if newImg.nChannel() == 1:
            newImg.data = cv2.cvtColor(newImg.data, cv2.COLOR_GRAY2BGR)
        color = (0, 255, 0)
        flags = 0
        newImg.data = cv2.drawKeypoints(newImg.data, self.kp, color, flags)
        return newImg
