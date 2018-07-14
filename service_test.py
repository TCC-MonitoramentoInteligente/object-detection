import argparse
import base64
import json
import os
import pathlib
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import cv2

service_url = 'http://localhost:8000/detect/'
window = 'object-detection'
script_path = os.path.dirname(os.path.abspath(__file__))


def arg_parse():
    """
    Parse arguments
    :return: args object
    """
    parser = argparse.ArgumentParser(description='Script to test service')
    parser.add_argument('--save', default=False, help='Save output to out/ folder', action='store_true')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--video", help="Path to video file", type=str)
    group.add_argument("--image", help="Path to image file", type=str)

    return parser.parse_args()


def request(data):
    data = urlencode(data).encode("utf-8")
    req = Request(service_url, data)
    return urlopen(req)


def draw_box(frame, obj, color_bgr=(0, 255, 0), thickness=2):
    """
    Draw a rectangle in an opencv frame
    :param frame: opencv frame
    :param obj: dict with detected object
    :param color_bgr: color
    :param thickness: thickness of rectangle
    :return: frame
    """
    top_left = (obj.get('x'), obj.get('y'))
    bottom_right = (obj.get('x2'), obj.get('y2'))
    return cv2.rectangle(frame, top_left, bottom_right, color_bgr, thickness)


def get_path_to_save(file_path):
    pathlib.Path('{}/out'.format(script_path)).mkdir(parents=True, exist_ok=True)
    head, tail = os.path.split(file_path)
    return '{}/out/{}'.format(script_path, tail)


def video(args):
    cap = cv2.VideoCapture(args.video)

    if args.save:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_file = get_path_to_save(args.video)
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    else:
        cv2.namedWindow(window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window, 600, 600)

    while cap.isOpened():
        ret, frame = cap.read()

        if frame is None:
            break

        start = time.time()
        response = request(data={'frame': base64.b64encode(frame), 'shape': frame.shape})
        end = time.time()
        print('FPS: {0:0.2f}'.format(1/(end - start)))
        json_response = response.read().decode('utf-8')
        object_list = json.loads(json_response)
        object_list = json.loads(object_list)

        for obj in object_list:
            frame = draw_box(frame, obj)

        if args.save:
            out.write(frame)
        else:
            cv2.imshow(window, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    if args.save:
        print('The video was saved in {}'.format(output_file))


def image(args):
    img = cv2.imread(args.image)
    if img is None:
        raise FileNotFoundError("Could not read image file '{}'.".format(args.image))

    start = time.time()
    response = request(data={'frame': base64.b64encode(img), 'shape': img.shape})
    end = time.time()
    print('Detection service took {0:0.2f} s to respond!'.format(end - start))
    json_response = response.read().decode('utf-8')
    object_list = json.loads(json_response)
    object_list = json.loads(object_list)

    for obj in object_list:
        img = draw_box(img, obj)

    if args.save:
        output_file = get_path_to_save(args.image)
        cv2.imwrite(output_file, img)
        print('The image was saved in {}'.format(output_file))
    else:
        cv2.namedWindow(window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window, 600, 600)
        cv2.imshow(window, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def main():
    args = arg_parse()

    if args.video is not None:
        video(args)
    elif args.image is not None:
        image(args)
    else:
        raise AttributeError("Must provide either video or image args")


if __name__ == '__main__':
    main()
