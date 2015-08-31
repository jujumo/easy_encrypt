__author__ = 'jumo'

import logging
import tarfile
from os.path import join, realpath, relpath, basename
from os import walk


def compact(input_path, ouput_filepath):
    input_path = realpath(input_path)
    tar = tarfile.open(ouput_filepath, "w")
    tar.add(input_path, arcname=basename('.'))
    tar.close()


def depack(input_filepath, ouput_path):
    tar = tarfile.open(input_filepath)
    tar.extractall(path=ouput_path)
    tar.close()


def main():
    import argparse
    try:
        parser = argparse.ArgumentParser(description='tar/detar files.')
        parser.add_argument('-v', '--verbose', action='store_true', help='verbose message')
        parser.add_argument('-c', '--compact', action='store_true', help='compact')
        parser.add_argument('-x', '--extract', action='store_true', help='verbose')
        parser.add_argument('-i', '--input', required=True, help='input file')
        parser.add_argument('-o', '--output', required=True, help='input file')

        args = parser.parse_args()
        if args.extract:
            depack(args.input, args.output)
        else:
            compact(args.input, args.output)

    except Exception as e:
        logging.critical(e)
        if __debug__:
            raise


if __name__ == '__main__':
    main()