import argparse
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
    response = urlopen(req)
    return response


def video(video_file):
    pass


def image(image_file):
    img = cv2.imread(image_file)
    b = img.tobytes()
    print(b)
    print(len(b))
    if img is None:
        raise FileNotFoundError("Could not read image file '{}'.".format(image_file))
    response = request(data={'image': b, 'shape': img.shape})
    print(response.read().decode('utf-8'))

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
