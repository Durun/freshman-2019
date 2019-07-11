from __future__ import annotations
import cv2
import numpy
import copy
from typing import List, Optional
from typing import Callable
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

    def filter(self, predicate: Callable[[cv2.DMatch], bool]) -> MatchPairs:
        NotImplementedError

    def sort(self) -> MatchPairs:
        new = copy.copy(self)
        new.matches = sorted(self.matches, key=lambda x: x.distance)
        return new

    def first(self, n: int) -> MatchPairs:
        size = min(n, len(self.matches))
        new = copy.copy(self)
        new.matches = self.matches[:size]
        return new

    def findHomography(self) -> Optional[List[float]]:
        srcKp = self.feature1.kp
        dstKp = self.feature2.kp

        matches = self.matches
        if 0 < len(matches):
            srcKps = [srcKp[m.queryIdx].pt for m in matches]
            dstKps = [dstKp[m.trainIdx].pt for m in matches]

            srcPts = numpy.float32(srcKps).reshape(-1, 1, 2)
            dstPts = numpy.float32(dstKps).reshape(-1, 1, 2)

            h, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC)
        else:
            h = None
        return h


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
