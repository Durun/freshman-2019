import cv2
from typing import List
from .feature import Feature
from .match_pairs import MatchPairs


class Matcher(object):
    """
    特徴点Matcher
    """
    matcherAlgorithm: cv2.DescriptorMatcher

    def __init__(self, matcherAlgorithm: cv2.DescriptorMatcher):
        self.matcherAlgorithm = matcherAlgorithm

    def match(self, feature1: Feature, feature2: Feature) -> MatchPairs:
        matches = feature1.match(feature2, self.matcherAlgorithm)
        return MatchPairs(feature1, feature2, matches)
