import argparse
import os
import sys

import numpy as np
from PIL import Image

sys.path.append('{}/..'.format(os.path.dirname(os.path.abspath(__file__))))

from detector import Detector


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def arg_parse():
    """
    Parse arguments
    :return: args object
    """
    parser = argparse.ArgumentParser(description='Script to extract fainting parameters')

    parser.add_argument("--path", help="Path to image files", required=True, type=str)

    return parser.parse_args()


def has_one_person(obj_list, fn):
    if len(obj_list) == 1:
        if obj_list[0]['label'] == 'person':
            return True
    print(Colors.FAIL + 'File "{}" needs to have exactly one person.'.format(fn) + Colors.ENDC)
    return False


def main(args):
    detector = Detector()
    detector.load_model()
    img_counter = 0
    csv = 'file; alpha; beta\n'

    while True:
        img_counter += 1
        file_name = 'v' + str(img_counter) + '{}.png'
        file_path = args.path + '/' + file_name
        try:
            normal_img = np.asarray(Image.open(file_path.format('n')))
            event_img = np.asarray(Image.open(file_path.format('e')))

            print('Processing "{}"...'.format(file_name.format('n')))
            normal_list = detector.detect(frame=normal_img)
            if not has_one_person(normal_list, file_name.format('n')):
                continue

            print('Processing "{}"...'.format(file_name.format('e')))
            event_list = detector.detect(frame=event_img)
            if not has_one_person(event_list, file_name.format('e')):
                continue

            person_normal = normal_list[0]
            event_person = event_list[0]

            hh = person_normal['height']
            alpha = event_person['height'] / event_person['width']
            beta = event_person['height'] / hh

            csv += '{}; {}; {}\n'.format('v' + str(img_counter), alpha, beta)

        except FileNotFoundError:
            print()
            break

    with open('test/alpha_beta.csv', 'w') as csv_file:
        csv_file.write(csv)


if __name__ == '__main__':
    arguments = arg_parse()
    main(arguments)
