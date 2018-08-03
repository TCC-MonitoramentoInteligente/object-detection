import threading


class ObjectDetector(threading.Thread):

    def __init__(self, vs, detector, messenger):
        super().__init__()
        self.vs = vs
        self.detector = detector
        self.messenger = messenger
        self.stop = False
        self.vs.start()
        self.id = vs.get_id()
        print('Creating object detector thread with id {}'.format(self.id))

    def run(self):
        while True:
            if self.stop:
                self.vs.kill()
                print('Killing object detector thread with id {}'.format(self.id))
                break
            elif self.vs.has_new_frame():
                frame = self.vs.get_frame()
                objects = self.detector.detect(frame)
                self.messenger({'id': self.id, 'objects': objects})

    def kill(self):
        self.stop = True

    def get_id(self):
        return self.id
