
import unittest
from ssl_encrypt import encrypt_file, decrypt_file


class MyTestCase(unittest.TestCase):
    def test_default_greeting_set(self):
        password = 'password'
        greeter = encrypt_file(in_file, out_file, password)
        print('test')
        # self.assertEqual(greeter.message, 'Hello world!')


if __name__ == '__main__':
    unittest.main()

