import cv2
from .detector import Detector

AKAZE = Detector(cv2.AKAZE_create())
ORB = Detector(cv2.ORB_create())
