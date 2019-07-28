
import PIL.Image
import pyocr
import logging
from typing import List
from freshman2019.camera.image import Image


class OcrNotAvailableError(Exception):
    "OCRツールが利用不可のときに投げるエラー"


class Recognizer(object):
    """
    画像から文字列を認識するクラス

    Throws
    ------
    OcrNotAvailableError
    """

    def __init__(self, tool, lang: str):
        self.tool = self.__getToolChecking(tool)
        self.lang = self.__getLangChecking(lang)

    def __getToolChecking(self, tool):
        """
        toolが使用可能ならそのまま返し, 使用不可なら例外を投げる.

        Parameters
        ----------
        tool
            pyocr.tesseract などを渡す

        Throws
        ------
        OcrNotAvailableError
        """
        if tool.is_available():
            logging.info("OCR tool %s is available." % tool.get_name())
        else:
            raise OcrNotAvailableError(tool + "is NOT available.")
        return tool

    def __getLangChecking(self, lang: str) -> str:
        """
        toolでlangが使用可能ならそのまま返し, 使用不可なら例外を投げる.

        Parameters
        ----------
        tool
            pyocr.tesseract など
        lang: str
            OCRエンジンで使用するデータセット名. "eng"など

        Throws
        ------
        OcrNotAvailableError
        """
        availables = self.tool.get_available_languages()  # List[str]
        if lang in availables:
            logging.info("OCR language dataset %s is available." % lang)
        else:
            raise OcrNotAvailableError("""%s + " is NOT available.
            Available languages: %s
            """ % (lang, availables))
        return lang

    def __recognize(self, image: Image, builder: pyocr.builders.BaseBuilder):
        """
        imageを認識し結果を返す
        結果の形式はbuilderによって変わる
        """
        pilImage = image.toPilImage()
        result = self.tool.image_to_string(
            pilImage,
            lang=self.lang,
            builder=builder
        )
        return result

    def imageToText(self, image: Image) -> str:
        """
        imageを認識し結果をstrで返す
        """
        builder = pyocr.builders.TextBuilder()
        result = self.__recognize(image, builder)
        return result

    def imageToBoxes(self, image: Image) -> List[pyocr.builders.Box]:
        """
        imageを認識し結果をpyocr.builders.Boxで返す

        Returns
        -------
        boxes: List[pyocr.builders.Box]
            box(下記)のリスト

            box.position: Tuple[ Tuple[int,int], Tuple[int,int] ]
                左上・右下座標(pixel)
            box.content: str
                内容の文字列
        """
        builder = pyocr.builders.WordBoxBuilder()
        result = self.__recognize(image, builder)
        return result

    def imageToLineBoxes(self, image: Image) -> pyocr.builders.LineBox:
        """
        imageを認識し結果をpyocr.builders.LineBoxで返す
        """
        builder = pyocr.builders.LineBoxBuilder()
        result = self.__recognize(image, builder)
        return result
