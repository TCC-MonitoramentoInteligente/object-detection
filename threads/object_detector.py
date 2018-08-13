import threading
import time


class ObjectDetector(threading.Thread):

    def __init__(self, vs, detector, messenger, on_finish):
        super().__init__()
        self.vs = vs
        self.detector = detector
        self.messenger = messenger
        self.stop = False
        self.vs.start()
        self.id = vs.get_id()
        self.fps = 0
        self.callback = on_finish
        print('Creating object detector thread with id {}'.format(self.id))

    def run(self):
        start = time.time()

        while True:
            if self.stop or not self.vs.isAlive():
                self.vs.kill()
                print('Killing object detector thread with id {}'.format(self.id))
                self.callback(self.id)
                self.id = None
                break

            if self.vs.has_new_frame():
                frame = self.vs.get_frame()
                objects = self.detector.detect(frame['frame'])
                self.fps = 1 / (time.time() - start)
                start = time.time()
                self.messenger({'id': self.id, 'time': frame['time'], 'objects': objects})

    def kill(self):
        self.stop = True

    def get_id(self):
        return self.id

    def get_video_fps(self):
        return self.vs.get_fps()

    def get_detection_fps(self):
        return self.fps
