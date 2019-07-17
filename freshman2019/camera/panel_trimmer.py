from .image import Image, GrayImage
from freshman2019.camera.util import CachingMatcher
from freshman2019.camera.matching import Matcher, MatchResult
from freshman2019.camera.matching import ORB


class PanelTrimmer(object):
    matcher: CachingMatcher

    def __init__(self, trainImage: Image, matcher: Matcher = ORB):
        self.matcher = CachingMatcher(matcher, trainImage.toGray())

    def __getMatchResult(self, queryImage: GrayImage) -> MatchResult:
        result = self.matcher.matchImage(queryImage)
        return result

    def trim(self, queryImage: Image) -> Image:
        query = queryImage.copy().toGray()
        query = query.normalize_clahe()
        # match
        matchResult = self.__getMatchResult(query)

        # filter
        matchResult = matchResult.percentileFilter(25)  # TODO
        matchResult = matchResult.first(200)  # TODO

        # warp
        h = matchResult.findHomography()
        resultImage = queryImage.copy().warp(h)
        return resultImage
