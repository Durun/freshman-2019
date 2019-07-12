import logging
import cv2
from freshman2019.camera import Camera
from freshman2019.camera.match_algorithms import ORB
from freshman2019.camera.feature import Feature
from freshman2019.camera.match_algorithms import MatchAlgorithm


def main():
    # logging.basicConfig(
    #     level=logging.INFO, format="%(levelname)s: %(funcName)s@%(filename)s(%(lineno)d): %(message)s")

    camera = Camera(
        0, "https://i.imgur.com/B0ra0iR.png")

    trainImg = camera.trainReader.read().resize(0.2).toGray()

    # detect feature
    algorithm = ORB
    detector = algorithm.detector
    trainFeature = detector.detect(trainImg)

    while True:
        loop(camera, algorithm, trainFeature)
        # キー入力を1ms待って、k が27（ESC）だったらBreakする
        k = cv2.waitKey(1)
        if k == 27:
            break
    cv2.destroyAllWindows()


def loop(camera: Camera, algorithm: MatchAlgorithm, trainFeature: Feature):
    queryColorImg = camera.queryReader.read()
    queryImg = queryColorImg.copy().toGray()
    queryColorImg.show("input")

    # detect feature
    detector = algorithm.detector
    queryFeature = detector.detect(queryImg)
    # match (query -> train)
    matcher = algorithm.matcher
    matchPairs = matcher.match(queryFeature, trainFeature)
    # filter
    matchPairs = matchPairs.sort()
    distances = [m.distance for m in matchPairs.matches]
    matchPairs = matchPairs.first(10)
    # warp
    h = matchPairs.findHomography()
    warpedImg = queryColorImg.warp(h)
    # show result
    matchPairs.plot().show("match")
    warpedImg.show("warp")

    for i, d in enumerate(distances):
        intD = int(d)
        cv2.line(queryColorImg.data, (i, 0), (i, intD), (255, 255, 0))
        delta = int(d - distances[i-1])*10
        cv2.line(queryColorImg.data, (i, 200), (i, 200+delta), (0, 0, 255))
    queryColorImg.show("distances")


main()
