import random
import unittest
import sys
sys.path.append('./lib')

import silme.diff

class EntityListDiffTestCase(unittest.TestCase):

    def setUp(self):
        self.elistdiff = silme.diff.EntityListDiff('test')

    def test_id(self):
        self.assertEqual(self.elistdiff.id, 'test')

    def test_diff(self):
        list1 = silme.core.EntityList('id1')
        list2 = silme.core.EntityList('id2')

        d = list1.diff(list2)
        self.assertEqual(d.id, 'id1')

    def test_diff_ordered(self):
        list1 = silme.core.EntityList('id1')
        list2 = silme.core.EntityList('id2')

        d = list1.diff(list2)
        self.assertEqual(d.ordered, list1.ordered)

    def test_diff_ordered2(self):
        list1 = silme.core.EntityList('id1', ordered=True)
        list2 = silme.core.EntityList('id2', ordered=True)

        d = list1.diff(list2)
        self.assertEqual(d.ordered, True)

    def test_diff_ordered3(self):
        list1 = silme.core.EntityList('id1', ordered=True)
        list2 = silme.core.EntityList('id2', ordered=True)
        list1.add(silme.core.Entity('id1', 'val1'))
        list1.add(silme.core.Entity('id2', 'val2'))
        list2.add(silme.core.Entity('id1', 'val3'))
        list2.add(silme.core.Entity('id2', 'val4'))

        d = list1.diff(list2)
        l=1
        for i in d.keys():
            self.assertEqual(i, 'id%s' % l)
            l+=1

if __name__ == '__main__':
    unittest.main()
