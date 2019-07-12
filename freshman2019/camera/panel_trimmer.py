from .image import Image
from .feature import Feature
from .match_pairs import MatchPairs
from freshman2019.camera.match_algorithms import ORB


class PanelTrimmer(object):
    trainFeature: Feature

    algorithm = ORB

    def __init__(self, trainImage: Image):
        self.trainFeature = self.__detectFeature(trainImage.toGray())

    def __detectFeature(self, image: Image) -> Feature:
        detector = self.__class__.algorithm.detector
        return detector.detect(image)

    def __matchFeature(self, queryFeature: Feature) -> MatchPairs:
        matcher = self.__class__.algorithm.matcher
        return matcher.match(queryFeature, self.trainFeature)

    def trim(self, queryImage: Image) -> Image:
        query = queryImage.copy().toGray()
        queryFeature = self.__detectFeature(query)

        # match
        matchPairs = self.__matchFeature(queryFeature)

        # filter
        matchPairs = matchPairs.sort()
        matchPairs = matchPairs.first(10)

        # warp
        h = matchPairs.findHomography()
        resultImage = queryImage.copy().warp(h)
        return resultImage
