import cv2
from typing import List
from .feature import Feature
from .match_points import KnnMatchPairs


class Matcher(object):
    """
    特徴点Matcher
    """

    def __init__(self, matcher):
        self.matcher = matcher

    def knnMatch(self, feature1: Feature, feature2: Feature, k: int) -> KnnMatchPairs:
        matches = self.matcher.knnMatch(feature1, feature2, k)
        return KnnMatchPairs(matches, k)
