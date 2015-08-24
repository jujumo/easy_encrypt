#!/usr/bin/env python3

__author__ = 'jumo'


import logging
import os
from os import urandom
import base64
import shutil

from hashlib import md5
try:
    from Crypto.Cipher import AES
except ImportError as e:
    logging.critical('Crypto not installed (or misspelled, make sure first letter is upper case in win dir).')
    raise
from convert_base64 import encode_filepath_base64, decode_filepath_base64


# source:
# http://stackoverflow.com/questions/16761458/how-to-aes-encrypt-decrypt-files-using-python-pycrypto-in-an-openssl-compatible
def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = b''  # changed '' to b''
    while len(d) < key_length + iv_length:
        # changed password to str.encode(password)
        d_i = md5(d_i + str.encode(password) + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]


def encrypt_file(in_file, out_file, password, salt_header='Salted__', key_length=32):
    # added salt_header=''
    bs = AES.block_size
    # replaced Crypt.Random with os.urandom
    salt = urandom(bs - len(salt_header))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # changed 'Salted__' to str.encode(salt_header)
    line = str.encode(salt_header) + salt
    out_file.write(line)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            # changed right side to str.encode(...)
            chunk += str.encode(padding_length * chr(padding_length))
            finished = True
        line = cipher.encrypt(chunk)
        out_file.write(line)


def decrypt_file(in_file, out_file, password, salt_header='Salted__', key_length=32):
    # added salt_header=''
    bs = AES.block_size
    # changed 'Salted__' to salt_header
    salt = in_file.read(bs)[len(salt_header):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(
            in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = chunk[-1]  # removed ord(...) as unnecessary
            chunk = chunk[:-padding_length]
            finished = True
            out_file.write(
                bytes(x for x in chunk))  # changed chunk to bytes(...)


def encrypt_filepath(input_filepath, output_filepath, password, base64_encoding=True):
    with open(input_filepath, 'rb') as in_file, open(output_filepath, 'wb') as out_file:
        logging.info('encrypting {} to {}'.format(input_filepath, output_filepath))
        encrypt_file(in_file, out_file, password)
    if base64_encoding:
        encode_filepath_base64(output_filepath, output_filepath)


def decrypt_filepath(input_filepath, output_filepath, password, base64_encoding=True):
    logging.debug('decrypting {} to {}'.format(input_filepath, output_filepath))
    if base64_encoding:
        input_tmp_filepath = input_filepath + '.tmp'
        decode_filepath_base64(input_filepath, input_tmp_filepath)

    with open(input_tmp_filepath, 'rb') as in_file, open(output_filepath, 'wb') as out_file:
        decrypt_file(in_file, out_file, password)

    if not input_tmp_filepath == input_filepath:
        os.remove(input_tmp_filepath)


def main():
    import argparse
    try:
        parser = argparse.ArgumentParser(description='Encrypt file with openSSL of the program.')
        parser.add_argument('-v', '--verbose', action='store_true', help='verbose message')
        parser.add_argument('-i', '--input', required=True, help='input file')
        parser.add_argument('-p', '--passwd', required=True, help='password')
        parser.add_argument('-o', '--output', help='output file')
        parser.add_argument('-d', '--decrypt', action='store_true', help='Specify it must decrypt the file')
        parser.add_argument('-e', '--encrypt', action='store_true', help='Specify it must encrypt the file. Default.')
        parser.add_argument('-b', '--base64', action='store_true', help='encode in base64')

        args = parser.parse_args()

        if args.verbose:
            if __debug__:
                logging.getLogger().setLevel(logging.DEBUG)
            else:
                logging.getLogger().setLevel(logging.INFO)

        input_filepath = os.path.abspath(args.input)
        if args.output:
            output_filepath = os.path.abspath(args.output)
        else:
            output_filepath = os.path.splitext(input_filepath)[0] + '.dat'

        if input_filepath == output_filepath:
            raise NameError('input and output files should be different')

        passphrase = args.passwd
        if args.decrypt:
            encrypt_filepath(input_filepath, output_filepath, passphrase, base64_encoding=args.base64)
        else:
            decrypt_filepath(input_filepath, output_filepath, passphrase, base64_encoding=args.base64)

    except Exception as e:
        logging.critical(e)
        if __debug__:
            raise


if __name__ == '__main__':
    main()