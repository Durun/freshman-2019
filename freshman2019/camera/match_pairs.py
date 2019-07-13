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

    def copy(self) -> MatchPairs:
        """
        自身のコピーを返す
        feature1, feature2は変化しないと仮定.
        matchesは複製する.
        """
        new = copy.copy(self)
        new.matches = copy.copy(self.matches)
        return new

    def plot(self) -> Image:
        img1 = self.feature1.img
        kp1 = self.feature1.kp
        img2 = self.feature2.img
        kp2 = self.feature2.kp
        newImg = img2.copy()
        if newImg.nChannel() == 1:
            newImg.data = cv2.cvtColor(newImg.data, cv2.COLOR_GRAY2BGR)
        newImg.data = cv2.drawMatches(img1.data, kp1,
                                      img2.data, kp2,
                                      self.matches,
                                      None, flags=2)
        return newImg

    def filter(self, predicate: Callable[[cv2.DMatch], bool]) -> MatchPairs:
        """
        マッチ結果をフィルタする
        Parameters
        ----------
        predicate: : Callable[[cv2.DMatch], bool]
            引数 cv2.DMatch の述語
            偽は除外される
        """
        new = self.copy()
        new.matches = list(filter(predicate, new.matches))
        return new

    def distanceFilter(self, upperBound: float) -> MatchPairs:
        """
        マッチ結果をdistance(特徴空間上の距離)でフィルタする
        Parameters
        ----------
        upperBound: float
            受容されるdistanceの上限
        """
        def pred(match: cv2.DMatch) -> bool: return (match.distance < upperBound)
        return self.filter(pred)

    def percentileFilter(self, upperBoundPercent: int) -> MatchPairs:
        """
        マッチ結果をdistance(特徴空間上の距離)の分布をもとに、
        パーセンタイルでフィルタする
        Parameters
        ----------
        upperBoundPercent: int
            受容されるパーセンタイルの上限
        """
        distances = self.getDistances()
        upperBound = numpy.percentile(distances, upperBoundPercent)
        return self.distanceFilter(upperBound)

    def sort(self) -> MatchPairs:
        new = self.copy()
        new.matches = sorted(new.matches, key=lambda x: x.distance)
        return new

    def first(self, n: int) -> MatchPairs:
        new = self.copy()
        size = min(n, len(new.matches))
        new.matches = new.matches[:size]
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

    def getDistances(self) -> List[float]:
        """
        distance(特徴空間上の距離)のリストへ変換する
        """
        return [m.distance for m in self.matches]


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
        newImg = img2.copy()
        if newImg.nChannel() == 1:
            newImg.data = cv2.cvtColor(newImg.data, cv2.COLOR_GRAY2BGR)
        newImg.data = cv2.drawMatchesKnn(img1.data, kp1,
                                         img2.data, kp2,
                                         self.matches,
                                         None, flags=self.k)
        return newImg
