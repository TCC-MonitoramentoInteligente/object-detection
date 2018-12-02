import argparse
import pandas


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
    parser = argparse.ArgumentParser(description='Script to analyse fainting parameters')

    parser.add_argument("--csv", help="Path to csv file", required=True, type=str)

    return parser.parse_args()


def main(args):
    df = pandas.read_csv(args.csv, sep=';')
    print(df.describe(exclude='file'))


if __name__ == '__main__':
    arguments = arg_parse()
    main(arguments)
