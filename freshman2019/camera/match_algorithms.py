import cv2
from .detector import Detector
from .matcher import Matcher


class MatchAlgorithm(object):
    detector: Detector
    matcher: Matcher

    def __init__(self, detector: Detector, matcher: Matcher):
        self.detector = detector
        self.matcher = matcher


ORB = MatchAlgorithm(detector=Detector(cv2.ORB_create()),
                     matcher=Matcher(cv2.BFMatcher(cv2.NORM_HAMMING)))
