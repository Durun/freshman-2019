import cv2
from freshman2019.camera import Camera
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s: %(funcName)s@%(filename)s(%(lineno)d): %(message)s")

camera = Camera(
    0, "https://gyazo.com/009c2f102ebb46ce326c4d153d5cf44a/thumb/1000")

# reader = camera.queryReader # カメラ画像
reader = camera.trainReader  # URL画像

colorImage = reader.read()
colorImage.show("color")

# 画像処理は破壊的に行われる. 元画像を残したければ .copy() する
grayImage = colorImage.copy().toGray()
smallImage = colorImage.copy().resize(0.5)
grayImage.show("gray")
smallImage.show("small")

binImage = grayImage.copy().blur_median(3).binarize()
binImage.show("bin")
binImage = binImage.morph_dilate(4)  # .copy() せずに処理する例
binImage.show("bin dilated")

print("Press any key on window to end.")
cv2.waitKey(0)
cv2.destroyAllWindows()
