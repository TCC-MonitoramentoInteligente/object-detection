import numpy as np

import cv2
import socket
import threading
import time


class ObjectDetector(threading.Thread):
    monitor_timeout = 60 * 5

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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.monitor_ip = None
        self.monitor_port = None
        self.monitor_start = None
        print('Creating object detector thread with id {}'.format(self.id))

    def run(self):
        start = time.time()

        while True:
            if self.stop or not self.vs.isAlive():
                self.vs.kill()
                print('Killing object detector thread with id {}'.format(self.id))
                self.callback(self.id, not self.vs.isAlive())
                self.id = None
                break

            if self.monitor_start:
                if (time.time() - self.monitor_start) > self.monitor_timeout:
                    self.monitor_ip, self.monitor_port = None, None

            if self.vs.has_new_frame():
                frame = self.vs.get_frame()
                objects = self.detector.detect(frame['frame'])
                if self.monitor_ip and self.monitor_port:
                    threading.Thread(target=self._send_detection, args=(frame['frame'], objects)).start()
                self.fps = 1 / (time.time() - start)
                start = time.time()
                self.messenger({'cam_id': self.id, 'time': frame['time'], 'objects': objects})

    def kill(self):
        self.stop = True

    def get_id(self):
        return self.id

    def get_video_fps(self):
        return self.vs.get_fps()

    def get_detection_fps(self):
        return self.fps

    def get_frame(self):
        return self.vs.get_frame()['frame']

    def get_port(self):
        return self.vs.get_port()

    def monitor(self, monitor_ip, monitor_port):
        """
        Send object detections video to monitor or debug
        :param monitor_ip: IP address to send detections
        :param monitor_port: IP port to send detections
        :return:
        """
        self.monitor_start = time.time()
        self.monitor_ip = monitor_ip
        try:
            self.monitor_port = int(monitor_port)
        except TypeError:
            self.monitor_port = None

    def _send_detection(self, frame, objects):
        """
        Method to debug detection of person
        :return:
        """
        try:
            for obj in objects:
                if obj.get('label') == 'person':
                    frame = _draw_box(frame, obj, (0, 255, 0))

            max_size = 65536 - 8  # less 8 bytes of video time
            jpg_quality = 80

            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality]
            result, encoded_img = cv2.imencode('.jpg', frame, encode_param)
            # Decrease quality until frame size is less than 65k
            while encoded_img.nbytes > max_size:
                jpg_quality -= 5
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality]
                result, encoded_img = cv2.imencode('.jpg', frame, encode_param)

            vt = np.array([0], dtype=np.float64)
            data = encoded_img.tobytes() + vt.tobytes()

            self.sock.sendto(data, (self.monitor_ip, self.monitor_port))
        except Exception as ex:
            print(ex)


def _draw_box(frame, obj, color_bgr, thickness=2):
    """
    Draw a rectangle in an numpy frame
    :param frame: numpy frame
    :param obj: dict with detected object
    :param color_bgr: color
    :param thickness: thickness of rectangle
    :return: numpy frame
    """
    top_left = (obj['x'], obj['y'])
    bottom_right = (obj['x'] + obj['width'], obj['y'] + obj['height'])
    return cv2.rectangle(frame, top_left, bottom_right, color_bgr, thickness)
