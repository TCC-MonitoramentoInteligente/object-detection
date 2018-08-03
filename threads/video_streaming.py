import socket
import threading

import cv2
import numpy as np


class VideoStreaming(threading.Thread):

    def __init__(self, ip, port):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.id = str(port)
        self.frame = None
        self.is_frame_new = False
        self.stop = False
        print('Creating video streaming thread with id {}'.format(self.id))

    def run(self):
        data = b''
        buffer_size = 65536

        while True:
            if self.stop:
                print('Killing video streaming thread with id {}'.format(self.id))
                self.sock.close()
                break
            data += self.sock.recv(buffer_size)
            a = data.find(b'\xff\xd8')
            b = data.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = data[a:b + 2]
                data = data[b + 2:]
                self.is_frame_new = True
                self.frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),
                                          cv2.IMREAD_COLOR)

    def get_frame(self):
        self.is_frame_new = False
        return self.frame

    def has_new_frame(self):
        return self.is_frame_new

    def get_id(self):
        return self.id

    def kill(self):
        self.stop = True
