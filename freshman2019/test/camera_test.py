import logging
from freshman2019.camera import Camera
import cv2


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(funcName)s@%(filename)s(%(lineno)d): %(message)s")

    camera = Camera(0, "https://i.imgur.com/ZstNqx4.png")

    def loop():
        panelImg = camera.getPanelImage()
        panelImg.show("panel")

    while True:
        loop()
        # キー入力を1ms待って、k が27（ESC）だったらBreakする
        k = cv2.waitKey(1)
        if k == 27:
            break
    cv2.destroyAllWindows()


main()
