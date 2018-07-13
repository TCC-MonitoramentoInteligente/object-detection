import argparse
import base64
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import cv2

service_url = 'http://localhost:8000/detect/'


def arg_parse():
    """
    Parse arguments
    :return: args object
    """
    parser = argparse.ArgumentParser(description='Script to test service')
    group = parser.add_mutually_exclusive_group()

    group.add_argument("--video", help="Path to video file", type=str)
    group.add_argument("--image", help="Path to image file", type=str)

    return parser.parse_args()


def request(data):
    data = urlencode(data).encode("utf-8")
    req = Request(service_url, data)
    return urlopen(req)


def video(video_file):
    pass


def image(image_file):
    img = cv2.imread(image_file)
    if img is None:
        raise FileNotFoundError("Could not read image file '{}'.".format(image_file))
    start = time.time()
    response = request(data={'frame': base64.b64encode(img), 'shape': img.shape})
    end = time.time()
    print(response.read().decode('utf-8'))
    print('Detection service took {0:0.2f} s to respond!'.format(end-start))

    # cv2.imshow('test', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def main():
    args = arg_parse()

    if args.video is not None:
        video(args.video)
    elif args.image is not None:
        image(args.image)
    else:
        raise AttributeError("Must provide either video or image args")


if __name__ == '__main__':
    main()
