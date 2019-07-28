"""
Usage: python -m freshman2019.test.camera_usage [DEVICE_NUM]

DEVICE_NUM は `ls /dev/video*` で調べる
"""

from freshman2019.camera import Camera
from freshman2019.camera import RecognitionError
import sys

deviceNum = int(sys.argv[1])
imageUrl = "https://i.imgur.com/BxmY2lg.png"

# カメラモジュール初期化
camera = Camera(deviceNum, imageUrl)

# 呼び出し: 温度の取得
try:
    temp = camera.get_temperature()
    print("Success! Temp= %d" % temp)
except RecognitionError as err:
    print("Failed.")
