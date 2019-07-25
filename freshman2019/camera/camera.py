from .image import ImageReader, UrlImageReader, CameraImageReader
from .image import Image
from .panel_trimmer import PanelTrimmer
from .ocr import Recognizer
from .recognition_error import RecognitionError
import pyocr
import logging


class Camera(object):
    queryReader: ImageReader
    trainReader: ImageReader
    trimmer: PanelTrimmer
    recognizer: Recognizer

    def __init__(self, deviceNumber: int, trainImageUrl: str):
        self.queryReader = CameraImageReader(deviceNumber)
        self.trainReader = UrlImageReader(trainImageUrl)
        trainImg = self.trainReader.read()
        self.trimmer = PanelTrimmer(trainImg)
        self.recognizer = Recognizer(
            tool=pyocr.tesseract, lang="letsgodigital")

    def get_temperature(self) -> int:
        """
        エアコンの設定温度を認識して返す

        Returns
        -------
        temp : int

        Throws
        ------
        RecognitionError
        """
        tempImg = self.getTemperetureImage()
        tempText = self.recognizer.imageToText(tempImg)
        try:
            tempInt = int(tempText)
        except ValueError:
            logging.warn("got " + tempText)
            raise RecognitionError("got " + tempText)

        if not self.isValidTemperature(tempInt):
            raise RecognitionError("got %d" % tempInt)

        return tempInt

    def is_power_on(self) -> bool:
        raise NotImplementedError

    # 内部の処理

    def isValidTemperature(self, t: int) -> bool:
        """
        整数が、エアコンの温度として妥当か?
        """
        return (10 < t) and (t < 40)

    def getPanelImage(self) -> Image:
        """
        パネル部分全体を切り出したImageを返す
        """
        queryImg = self.queryReader.read()
        panelImg = self.trimmer.trim(queryImg)
        return panelImg

    def getTemperetureImage(self) -> Image:
        """
        パネルの温度表示部分を切り出したImageを返す
        """
        panelImage = self.getPanelImage()
        panelImage.trim(p1=(465, 240), p2=(525, 305))

        return panelImage
