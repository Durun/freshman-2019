from __future__ import annotations
from .image import Image, GrayImage
from freshman2019.camera.util import CachingMatcher
from freshman2019.camera.matching import Matcher, MatchResult
from freshman2019.camera.matching import ORB
import numpy
from statistics import mean
import logging


class PanelTrimmer(object):
    matcher: CachingMatcher
    stabler: Stabler

    def __init__(self, trainImage: Image, matcher: Matcher = ORB):
        self.matcher = CachingMatcher(matcher, trainImage.toGray())
        self.stabler = Stabler(alpha=0.16)  # TODO

    def __getMatchResult(self, queryImage: GrayImage) -> MatchResult:
        result = self.matcher.matchImage(queryImage)
        return result

    def trim(self, queryImage: Image) -> Image:
        query = queryImage.copy().toGray()
        # query = query.normalize_clahe()
        # match
        matchResult = self.__getMatchResult(query)

        # filter
        matchResult = matchResult.percentileFilter(25)  # TODO
        matchResult = matchResult.first(200)  # TODO

        # warp
        h = matchResult.findHomography()
        if not h is None:
            h = self.stabler.stableSuppressing(h)
        resultImage = queryImage.copy().warp(h)
        return resultImage


class Stabler(object):
    """
    指数平滑法

    alpha: 0.0~1.0
        小さいほうがスムーズ
    """
    alpha: float
    lastInput: numpy.ndarray
    lastOutput: numpy.ndarray

    def __init__(self, alpha: float):
        self.alpha = alpha
        one = numpy.array([[1, 0, 0],
                           [0, 1, 0],
                           [0, 0, 1]])
        self.lastInput = one
        self.lastOutput = one

    def stable(self, nowInput: numpy.ndarray, blend: float = 1.0) -> numpy.ndarray:
        # blend
        nowInput = blend*nowInput + (1-blend)*self.lastOutput

        # calc
        w1 = self.alpha
        w2 = 1 - self.alpha
        nowOutput = w1 * self.lastInput + w2 * self.lastOutput

        # update
        self.lastInput = nowInput
        self.lastOutput = nowOutput

        return nowOutput

    def stableSuppressing(self, nowInput: numpy.ndarray) -> numpy.ndarray:
        # flat = (nowInput - self.lastOutput).flatten()
        # delta = sum([abs(v) for v in flat])
        det = numpy.linalg.det(nowInput)
        if det < 0.5:
            blend = 0.0
            logging.info("ignoring calibratioin: (det= %f)" % det)
        else:
            blend = 1.0
        return self.stable(nowInput, blend=blend)
