import logging
import cv2
from freshman2019.camera import Camera
from freshman2019.camera.image import Image
import numpy
import math
from typing import Tuple


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s: %(funcName)s@%(filename)s(%(lineno)d): %(message)s")

    camera = Camera(
        2, "https://i.imgur.com/B0ra0iR.png")

    while True:
        loop(camera)
        # キー入力を1ms待って、k が27（ESC）だったらBreakする
        k = cv2.waitKey(1)
        if k == 27:
            break
    cv2.destroyAllWindows()


def loop(camera: Camera):
    inputImage = camera.queryReader.read()

    grayImage = inputImage.copy().toGray()
    # denoise
    grayImage = grayImage.denoise()
    grayImage = grayImage.normalize_clahe(clipLimit=2.0, gridSize=8)
    # detect edges
    edges = cv2.Canny(grayImage.data, 100, 180, apertureSize=3)
    # detect lines
    lines = cv2.HoughLinesP(edges, 1, numpy.pi / 180,
                            threshold=100, minLineLength=40, maxLineGap=20)
    if lines is None:
        lines = []
    lines = [
        ((line[0][0], line[0][1]), (line[0][2], line[0][3]))
        for line in lines
    ]

    # detect degree
    degrees = [lineToDegree(line) for line in lines]
    degrees = sorted(degrees) or []
    plotImage = inputImage.copy()
    plotDistribution(plotImage, (45, 0), degrees)

    degrees = numpy.array(degrees)
    plotDistribution(plotImage, (45+90, 0), degrees)
    degrees = outlierFilter(degrees)
    plotDistribution(plotImage, (45+180, 0), degrees)
    if len(degrees) == 0:
        degrees = [0.0]
    meanDegree = sum(degrees) / len(degrees)

    # plot lines
    for p1, p2 in lines:
        cv2.line(plotImage.data, p1, p2, (255, 255, 0))

    # show
    cv2.imshow("edges", edges)
    grayImage.show("processing")
    plotImage.show("lines")
    inputImage.rotate(meanDegree).show("rot")


def lineToDegree(line) -> float:
    p1, p2 = line
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    arg = math.atan2(dy, dx)
    deg = (math.degrees(arg) + 180 + 45) % 90 - 45
    return deg


def outlierFilter(array):
    ratio = 1.5
    if 0 < len(array):
        quartile1, quartile3 = numpy.percentile(array, [25, 75])
        iqr = quartile3 - quartile1
        lowerBound = quartile1 - (iqr * ratio)
        upperBound = quartile3 + (iqr * ratio)
        def prod(x): return ((lowerBound < x) and (x < upperBound))
        array = list(filter(prod, array))
    return array


def plotDistribution(dst: Image, position: Tuple[int, int], values):
    posX, posY = position
    length = len(values)
    if 0 < length:
        quartile1, quartile3 = numpy.percentile(values, [25, 75])
        q1, q3 = (int(quartile1), int(quartile3))
    # plot values
    for i, value in enumerate(values):
        d = int(value)
        cv2.line(dst.data, (posX, posY+i), (posX + d, posY+i), (0, 255, 0))
    # plot percentile
        cv2.line(dst.data,
                 (posX + q1, posY), (posX + q1, posY + length),
                 (255, 0, 0))
        cv2.line(dst.data,
                 (posX + q3, posY), (posX + q3, posY + length),
                 (255, 0, 0))


main()
