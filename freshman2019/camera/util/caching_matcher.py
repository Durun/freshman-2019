from freshman2019.camera.image import GrayImage
from freshman2019.camera.matching import Feature, Matcher, MatchResult


class CachingMatcher(object):

    def __init__(self, matcher: Matcher, trainImage: GrayImage):
        self.matcher = matcher
        self.trainFeature = matcher.detect(trainImage)

    def matchImage(self, queryImage: GrayImage):
        queryFeature = self.matcher.detect(queryImage)
        result = self.matcher.match(queryFeature, self.trainFeature)
        return result
