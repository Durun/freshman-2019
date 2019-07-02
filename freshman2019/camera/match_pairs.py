import cv2
from typing import List


class MatchPairs(object):
    """
        特徴点マッチ結果
    """

    pass


class KnnMatchPairs(object):
    matches: List[List[cv2.DMatch]]
    k: int

    def __init__(self, matches: List[List[cv2.DMatch]], k: int):
        self.matches = matches
        self.k = k
