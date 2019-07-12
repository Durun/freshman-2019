import logging
import cv2
from freshman2019.camera import Camera
from freshman2019.camera.match_algorithms import ORB


logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s: %(funcName)s@%(filename)s(%(lineno)d): %(message)s")

camera = Camera(
    0, "https://i.imgur.com/B0ra0iR.png")

trainImg = camera.trainReader.read().resize(0.2).toGray()
queryColorImg = camera.queryReader.read()
queryImg = queryColorImg.copy().toGray()

# detect feature
algorithm = ORB
detector = algorithm.detector
trainFeature = detector.detect(trainImg)
queryFeature = detector.detect(queryImg)

# match (query -> train)
matcher = algorithm.matcher
matchPairs = matcher.match(queryFeature, trainFeature)
# filter
matchPairs = matchPairs.sort().first(20)
# warp
h = matchPairs.findHomography()
warpedImg = queryColorImg.copy().warp(h)

# show result
matchPairs.plot().show("match")
warpedImg.show("warp")


print("Press any key on window to end.")
cv2.waitKey(0)
cv2.destroyAllWindows()
