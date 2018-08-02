import argparse
import threading
import time

from video.video_streaming import VideoStreaming


def arg_parse():
    parser = argparse.ArgumentParser(description='Object detection service')
    parser.add_argument('--ip', help='Client IP address', default='localhost')
    parser.add_argument('--ports', help='UDP ports number list', nargs='+', type=int)
    return parser.parse_args()


def detect(vs, detector):
    while True:
        if vs.has_new_frame():
            frame = vs.get_frame()
            objects = detector.detect(frame)
            send_detections({'id': vs.get_id(), 'objects': objects})


def send_detections(result):
    print(result.get('id') + ' ' + result.get('objects').get('detection') + ' ' + str(time.time()))


def main(args):
    detector = FalseDetector()
    detector.load_model()

    for port in args.ports:
        print('Starting thread to receive video on port {}'.format(port))
        vs = VideoStreaming({'ip': args.ip, 'port': port})
        vs.start()
        print('Starting thread to object detection')
        threading.Thread(target=detect, args=(vs, detector,)).start()


class FalseDetector:
    def load_model(self):
        print('Loading network')
        time.sleep(2)
        print('Network successfully loaded')

    def detect(self, frame):
        time.sleep(0.18)
        return {'detection': 'OK'}


if __name__ == '__main__':
    arguments = arg_parse()
    main(arguments)
