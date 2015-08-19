import random
import unittest
import sys
sys.path.append('./lib')

import silme.core
import silme.core.logger

class EntityTestCase(unittest.TestCase):

    def setUp(self):
        self.entitylist = silme.core.EntityList('id1')

    def test_log(self):
        self.entitylist.log('INFO', 'test message')
        self.assertEqual(self.entitylist.logs, [('INFO', 'test message', None)])

    def test_get_logs(self):
        self.entitylist.log('INFO', 'test message')
        self.entitylist.log('INFO', 'test message2')
        self.assertEqual(len(self.entitylist.get_logs()), 2)
    
    def test_get_all_logs(self):
        self.entitylist.log('INFO', 'test entitylist message')
        package = silme.core.Package('id1')
        package.log('ERROR', 'test package message')
        package2 = silme.core.Package('id2')
        package2.log('ERROR', 'test package message2')
        package2.add_structure(self.entitylist)
        package.add_package(package2)
        self.assertEqual(len(package.get_logs(recursive=True)), 3)

if __name__ == '__main__':
    unittest.main()
