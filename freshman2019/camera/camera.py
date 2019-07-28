from .image import ImageReader, UrlImageReader, CameraImageReader
from .image import Image, GrayImage
from .panel_trimmer import PanelTrimmer
from .ocr import Recognizer
from .recognition_error import RecognitionError
import pyocr
import logging
from typing import List


class Camera(object):

    def __init__(self, deviceNumber: int, trainImageUrl: str):
        """
        カメラの初期化

        Parameters
        ----------
        deviceNumber: int
            カメラのビデオデバイス番号
            linuxなら `ls /dev/video*` でわかる
        trainImageUrl: str
            パネルを正面から撮った画像のURL
        """
        self.queryReader = CameraImageReader(deviceNumber)
        self.trainReader = UrlImageReader(trainImageUrl)
        trainImg = self.trainReader.read()
        self.trimmer = PanelTrimmer(trainImg)
        self.recognizer = Recognizer(
            tool=pyocr.tesseract, lang="letsgodigital")

    def get_temperature(self, timeout: int = 50, sampleSize: int = 5) -> int:
        """
        エアコンの設定温度を認識して返す

        Parameters
        ----------
        timeout : int
            認識の試行回数
        sampleSize : int
            認識をsampleSize回試して、最頻値を結果とする

        Returns
        -------
        temp : int

        Throws
        ------
        RecognitionError
        """
        from statistics import median
        tryCount = 0
        samples = []
        for i in range(timeout):
            tryCount = i+1
            try:
                samples.append(self.getTemperatureOnce())
            except RecognitionError:
                pass
            if len(samples) >= sampleSize:
                break
        logging.info("tried %d times -> got %s" % (tryCount, str(samples)))

        if len(samples) == 0:
            raise RecognitionError

        result = median(samples)
        return int(result)

    def is_power_on(self) -> bool:
        raise NotImplementedError

    # 内部の処理

    def getTemperatureOnce(self) -> int:
        """
        エアコンの設定温度を1回認識して返す

        Returns
        -------
        temp : int

        Throws
        ------
        RecognitionError
        """
        tempImg = self.getTemperetureImage()  # type : Image
        tempBoxes = self.recognizer.imageToLineBoxes(tempImg)
        temps = self.lineBoxestoTempList(tempBoxes)  # type : List[str]
        if len(temps) == 0:
            raise RecognitionError
        return temps.pop()

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
        import cv2
        panelImage = self.getPanelImage()
        tempImage = panelImage.trim(p1=(400, 150), p2=(600, 350))  # TODO
        # mask
        binImage = self.binarizePanel(tempImage.toGray())
        maskImage = self.createMask(binImage)
        tempImage = binImage.bitwise_not().mask(maskImage)
        tempImage.morph_close(3)
        return tempImage

    def binarizePanel(self, image: GrayImage) -> GrayImage:
        """
        パネル画像を2値化
        """
        image = image.copy()
        image = image.normalize_clahe(gridSize=4).blur_median(5).binarize()
        image = image.morph_close2()
        image = image.morph_close(2)
        return image

    def createMask(self, binImage: GrayImage) -> GrayImage:
        """
        数字部分だけを抜き出すためのマスクを作成
        """
        import cv2
        image = binImage.copy()
        image = image.normalize_clahe(gridSize=4).blur_median(5).binarize()
        image = image.morph_close2()
        image = image.morph_close(2)
        image = image.morph_open(3)
        image = image.morph_close(3)

        maskImg = image.copy()
        maskImg.data.fill(0)
        contours, hierarchy = cv2.findContours(
            image.data, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            # 輪郭に外接する長方形を取得する。
            x, y, width, height = cv2.boundingRect(cnt)
            # 面積を計算
            s = width * height
            # 縦横比を計算
            r = width / height
            # 塗りつぶし
            if (300 < s) and (s < 2000) and (0.4 < r) and (r < 0.8):
                # print("s= %f , r= %f" % (s, r))
                cv2.rectangle(maskImg.data, (x, y), (x+width, y+height),
                              (255, 255, 255), -1, cv2.LINE_AA)
        return maskImg

    def lineBoxestoTempList(self, boxes: List[pyocr.builders.LineBox]) -> List[int]:
        """
        温度として妥当な文字列のみを返す
        """
        texts = [box.content for box in boxes]

        # 小数点を除去
        map(lambda s: s.strip("."), texts)

        # 整数に変換
        temps = []
        for text in texts:
            try:
                integer = int(text)
                temps.append(integer)
            except ValueError:
                pass

        # 外れ値を除去
        def isValidTemperature(t: int) -> bool:
            return (10 < t) and (t < 30)
        validTemps = filter(lambda t: isValidTemperature(t), temps)
        return list(validTemps)
