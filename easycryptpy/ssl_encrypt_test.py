
import unittest
from ssl_encrypt import encrypt_file, decrypt_file
import tempfile


class FileCipherTest(unittest.TestCase):
    def test_cipher_decipher(self):
        password = 'password'
        content_expected = bytearray('papa', encoding='utf-8')
        with tempfile.NamedTemporaryFile() as clear_f, tempfile.NamedTemporaryFile() as cipher_file:
            clear_f.write(content_expected)
            clear_f.seek(0)
            cipher_file.seek(0)
            greeter = encrypt_file(clear_f, cipher_file, password)
            clear_f.seek(0)
            cipher_file.seek(0)
            greeter = decrypt_file(cipher_file, clear_f, password)
            clear_f.seek(0)
            cipher_file.seek(0)
            content_retrieved = clear_f.read()
            self.assertTrue\
                (content_retrieved == content_expected)


if __name__ == '__main__':
    unittest.main()

