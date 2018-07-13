import os
import sys

sys.path.append("{}/../../".format(os.path.dirname(os.path.abspath(__file__))))

from detector import Detector

detector = Detector()
detector.load_model()
