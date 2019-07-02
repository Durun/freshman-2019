import cv2
import copy
from typing import List
from .image import Image
from .feature import Feature


class MatchPairs(object):
    """
        特徴点マッチ結果
    """

    feature1: Feature
    feature2: Feature
    matches: List[cv2.DMatch]

    def __init__(self, feature1: Feature, feature2: Feature, matches: List[cv2.DMatch],):
        self.feature1 = feature1
        self.feature2 = feature2
        self.matches = matches

    def plot(self) -> Image:
        img1 = self.feature1.img
        kp1 = self.feature1.kp
        img2 = self.feature2.img
        kp2 = self.feature2.kp
        newImg = copy.copy(img2)
        if newImg.nChannel() == 1:
            newImg.data = cv2.cvtColor(newImg.data, cv2.COLOR_GRAY2BGR)
        newImg.data = cv2.drawMatches(img1.data, kp1,
                                      img2.data, kp2,
                                      self.matches,
                                      None, flags=2)
        return newImg


class KnnMatchPairs(object):
    feature1: Feature
    feature2: Feature
    matches: List[List[cv2.DMatch]]
    k: int

    def __init__(self, feature1: Feature, feature2: Feature, matches: List[List[cv2.DMatch]], k: int):
        self.feature1 = feature1
        self.feature2 = feature2
        self.matches = matches
        self.k = k

    def plot(self) -> Image:
        img1 = self.feature1.img
        kp1 = self.feature1.kp
        img2 = self.feature2.img
        kp2 = self.feature2.kp
        newImg = copy.copy(img2)
        if newImg.nChannel() == 1:
            newImg.data = cv2.cvtColor(newImg.data, cv2.COLOR_GRAY2BGR)
        newImg.data = cv2.drawMatchesKnn(img1.data, kp1,
                                         img2.data, kp2,
                                         self.matches,
                                         None, flags=self.k)
        return newImg
