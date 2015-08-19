import random
import unittest
import sys
sys.path.append('./lib')

import silme.io.clients

class ClientsTestCase(unittest.TestCase):

    def setUp(self):
        self.io = silme.io.clients.FileFormatClient

    def test__should_ignore(self):
        def test_ignore(path, elems):
            return 'c' in elems

        self.assertFalse(self.io._should_ignore(['a', 'b'], './path', ['c','d']))
        self.assertTrue(self.io._should_ignore(['a', 'b', 'c'], './path', ['c','d']))
        self.assertFalse(self.io._should_ignore(test_ignore, './path', ['a','d']))
        self.assertTrue(self.io._should_ignore(test_ignore, './path', ['c','d']))

if __name__ == '__main__':
    unittest.main()
