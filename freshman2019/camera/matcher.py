import cv2
from typing import List
from .image import Image
from .feature import Feature
from .match_pairs import MatchPairs


class Matcher(object):
    """
    特徴点DetectorとMatcher
    """
    detectorAlgorithm: cv2.Feature2D
    matcherAlgorithm: cv2.DescriptorMatcher

    def __init__(self,
                 detectorAlgorithm: cv2.Feature2D,
                 matcherAlgorithm: cv2.DescriptorMatcher):
        self.detectorAlgorithm = detectorAlgorithm
        self.matcherAlgorithm = matcherAlgorithm

    def detect(self, image: Image) -> Feature:
        kp, des = self.detectorAlgorithm.detectAndCompute(image.data, None)
        return Feature(image, kp, des)

    def match(self, feature1: Feature, feature2: Feature) -> MatchPairs:
        matches = feature1.match(feature2, self.matcherAlgorithm)
        return MatchPairs(feature1, feature2, matches)
