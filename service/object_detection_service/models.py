import time


class FalseDetector:
    def load_model(self):
        print('Loading network')
        time.sleep(2)
        print('Network successfully loaded')

    def detect(self, frame):
        time.sleep(0.18)
        return {'detection': 'OK'}


client_ip = ""
object_detector_threads = []
detector = FalseDetector()
