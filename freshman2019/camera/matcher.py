from typing import List
from .feature import Feature
from .match_pairs import MatchPairs, KnnMatchPairs


class Matcher(object):
    """
    特徴点Matcher
    """

    def __init__(self, matcher):
        self.matcher = matcher

    def match(self, feature1: Feature, feature2: Feature) -> MatchPairs:
        matches = self.matcher.match(feature1.des, feature2.des)
        return MatchPairs(feature1, feature2, matches)

    def knnMatch(self, feature1: Feature, feature2: Feature, k: int) -> KnnMatchPairs:
        matches = self.matcher.knnMatch(feature1.des, feature2.des, k)
        return KnnMatchPairs(feature1, feature2, matches, k)
