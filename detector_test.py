import argparse

import cv2

from detector import Detector


def arg_parse():
    """
    Parse arguments to the algorithm
    :return: args object
    """
    parser = argparse.ArgumentParser(description='Script to test detector interface')

    parser.add_argument("--image", help="Path to image file", required=True, type=str)

    return parser.parse_args()


def main():
    args = arg_parse()
    img = cv2.imread(args.image)
    if img is None:
        print("Could not read image file '{}'.".format(args.image))
    else:
        detector = Detector()
        detector.load_model()
        object_list = detector.detect(frame=img)
        print()
        for obj in object_list:
            print(obj.to_string())


if __name__ == '__main__':
    main()
