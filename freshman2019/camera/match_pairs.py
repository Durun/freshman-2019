import cv2
from typing import List
from .feature import Feature


class MatchPairs(object):
    """
        特徴点マッチ結果
    """

    pass


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
