import unittest
import os
import os.path as path
from ssl_encrypt import encrypt_file, decrypt_file, encrypt_filepath, decrypt_filepath
import tempfile
import subprocess

FNULL = open(os.devnull, 'w')

class FileCipherTest(unittest.TestCase):
    def test_python_cipher_python_decipher(self):
        password = 'password'
        content_expected = bytearray('papa', encoding='utf-8')
        with tempfile.NamedTemporaryFile() as clear_f, tempfile.NamedTemporaryFile() as cipher_file:
            clear_f.write(content_expected)
            clear_f.seek(0)
            cipher_file.seek(0)
            encrypt_file(clear_f, cipher_file, password)
            clear_f.seek(0)
            cipher_file.seek(0)
            decrypt_file(cipher_file, clear_f, password)
            clear_f.seek(0)
            cipher_file.seek(0)
            content_retrieved = clear_f.read()
            self.assertTrue\
                (content_retrieved == content_expected)

    def test_python_cipher_opensssl_decipher(self):
        password = 'password'
        plaintext = 'content'
        working_dir = r'a:\vault'
        plain_filepath = path.join(working_dir, 'sample.txt')
        coded_filepath = path.join(working_dir, 'sample.txt.enc')
        decoded_filepath = path.join(working_dir, 'sample.txt.enc.txt')
        with open(plain_filepath, 'w') as plain:
            plain.write(plaintext)
        # encrypt
        encrypt_filepath(plain_filepath, coded_filepath, password=password)
        # decrypt
        cmd_line = ['openssl', 'aes-256-cbc', '-d', '-base64', '-md', 'md5', '-salt', '-k', password,
                    '-in', coded_filepath, '-out', decoded_filepath]
        res = subprocess.call(cmd_line, stdout=FNULL, stderr=subprocess.STDOUT)
        self.assertEqual(res, 0)

        with open(decoded_filepath, 'r') as decoded_file:
            decoded = decoded_file.read()

        self.assertEqual(decoded, plaintext)

    def test_openssl_cipher_python_decipher(self):
        password = 'password'
        plaintext = 'content'
        working_dir = r'a:\vault'
        plain_filepath = path.join(working_dir, 'sample.txt')
        coded_filepath = path.join(working_dir, 'sample.txt.enc')
        decoded_filepath = path.join(working_dir, 'sample.txt.enc.txt')
        with open(plain_filepath, 'w') as plain:
            plain.write(plaintext)
        # encrypt
        cmd_line = ['openssl', 'aes-256-cbc', '-e', '-base64', '-md', 'md5', '-salt', '-k', password,
                    '-in', plain_filepath, '-out', coded_filepath]
        res = subprocess.call(cmd_line, stdout=FNULL, stderr=subprocess.STDOUT)
        # decrypt
        decrypt_filepath(coded_filepath, decoded_filepath, password=password)

        with open(decoded_filepath, 'r') as decoded_file:
            decoded = decoded_file.read()
        self.assertEqual(decoded, plaintext)


if __name__ == '__main__':
    unittest.main()

