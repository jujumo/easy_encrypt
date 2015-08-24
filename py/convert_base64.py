#!/usr/bin/env python3

__author__ = 'jumo'

import shutil
import base64
import logging


def encode_file_base64(in_file, out_file, chunk_size=64):
    finished = False
    data = b''
    while not finished:
        chunk = in_file.read(1024 * chunk_size)
        if len(chunk) == 0:
            # no more chunk
            finished = True
        elif len(chunk) % chunk_size != 0:
            # last chunk
            finished = True
        data += chunk

    data_b64 = base64.b64encode(data)
    finished = False
    while not finished:
        line = data_b64[:chunk_size]
        if len(line) == 0 or len(line) < chunk_size:
            finished = True
        else:
            data_b64 = data_b64[chunk_size:]
        out_file.write(line + b'\n')


def decode_file_base64(in_file, out_file, chunk_size=64):
    finished = False
    data_b64 = r''
    while not finished:
        chunk = in_file.read(1024 * chunk_size).decode('UTF-8')
        if len(chunk) == 0:
            # no more chunk
            finished = True
        elif len(chunk) % chunk_size != 0:
            # last chunk
            finished = True
        data_b64 += chunk

    data = base64.b64decode(data_b64)
    finished = False
    while not finished:
        line = data[:chunk_size]
        if len(line) == 0 or len(line) < chunk_size:
            finished = True
        else:
            data = data[chunk_size:]
        out_file.write(line)


def encode_filepath_base64(input_filepath, output_filepath):
    output_tmp_filepath = output_filepath + '.tmp'  # always tmp file
    with open(input_filepath, 'rb') as in_file, open(output_tmp_filepath, 'wb') as out_file:
        encode_file_base64(in_file, out_file)
    shutil.move(output_tmp_filepath, output_filepath)


def decode_filepath_base64(input_filepath, output_filepath):
    output_tmp_filepath = output_filepath + '.tmp'  # always tmp file
    with open(input_filepath, 'rb') as in_file, open(output_tmp_filepath, 'wb') as out_file:
        decode_file_base64(in_file, out_file)
    shutil.move(output_tmp_filepath, output_filepath)


def main():
    import argparse
    try:
        parser = argparse.ArgumentParser(description='Encrypt file with openSSL of the program.')
        parser.add_argument('-v', '--verbose', action='store_true', help='verbose message')
        parser.add_argument('-d', '--decode', action='store_true', help='verbose message')
        parser.add_argument('-e', '--encode', action='store_true', help='verbose message')
        parser.add_argument('-i', '--input', required=True, help='input file')
        parser.add_argument('-o', '--output', required=True, help='input file')

        args = parser.parse_args()
        if args.decode:
            decode_filepath_base64(args.input, args.output)
        else:
            encode_filepath_base64(args.input, args.output)

    except Exception as e:
        logging.critical(e)
        if __debug__:
            raise

if __name__ == '__main__':
    main()