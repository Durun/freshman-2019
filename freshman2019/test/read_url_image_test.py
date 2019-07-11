import cv2
from freshman2019.camera.image_reader import UrlImageReader

reader = UrlImageReader(
    "https://gyazo.com/009c2f102ebb46ce326c4d153d5cf44a/thumb/1000")
image = reader.read()
image.show("image")

print("Press any key on window to end.")
cv2.waitKey(0)
cv2.destroyAllWindows()
