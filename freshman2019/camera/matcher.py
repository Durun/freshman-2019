from typing import List
from .feature import Feature
from .match_pairs import MatchPairs


class Matcher(object):
    """
    特徴点Matcher
    """

    def __init__(self, matcher):
        self.matcher = matcher

    def match(self, feature1: Feature, feature2: Feature) -> MatchPairs:
        matches = self.matcher.match(feature1.des, feature2.des)
        return MatchPairs(feature1, feature2, matches)
