import logging
from freshman2019.camera import Camera
from freshman2019.camera import RecognitionError
import cv2
import sys

deviceNum = int(sys.argv[1])
imageUrl = "https://i.imgur.com/BxmY2lg.png"


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(funcName)s@%(filename)s(%(lineno)d): %(message)s")

    camera = Camera(deviceNum, imageUrl)

    def loop():

        try:
            temp = camera.get_temperature()
            print("Temp= %d" % temp)
        except RecognitionError as err:
            print("Failed")

    while True:
        loop()
        # キー入力を1ms待って、k が27（ESC）だったらBreakする
        k = cv2.waitKey(1)
        if k == 27:
            break
    cv2.destroyAllWindows()


main()
