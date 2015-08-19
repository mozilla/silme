import random
import unittest
import sys
sys.path.append('./lib')

import silme.diff

class EntityDiffTestCase(unittest.TestCase):

    def setUp(self):
        self.entitydiff = silme.diff.EntityDiff('test')

    def test_id(self):
        self.assertEqual(self.entitydiff.id, 'test')

    def test_add_hunk(self):
        self.entitydiff['id'] = ('test', 'newid')
        self.assertEqual(len(self.entitydiff.items()), 1)

    def test_get_hunk(self):
        self.entitydiff['id'] = ('test', 'newid')
        self.assertEqual(self.entitydiff['id'], ('test', 'newid'))

    def test_add_value(self):
        self.entitydiff['value'] = ('oldval', 'newval')
        self.assertEqual(self.entitydiff['value'], ('oldval', 'newval'))

    def test_diff_id(self):
        entity1 = silme.core.Entity('id1')
        entity2 = silme.core.Entity('id2')
        d = entity1.diff(entity2)
        self.assertEqual(d['id'], ('id1', 'id2'))

    def test_diff_simplevalue(self):
        entity1 = silme.core.Entity('id1')
        entity1.value = "Hey Jude"
        entity2 = silme.core.Entity('id1')
        entity2.value = "Hey Jolie"
        d = entity1.diff(entity2)
        self.assertEqual(d['value'], ('Hey Jude', 'Hey Jolie'))

    def test_apply_diff_id(self):
        entity1 = silme.core.Entity('id1')
        entity2 = silme.core.Entity('id2')
        d = entity1.diff(entity2)

        entity1.apply_diff(d)
        self.assertEqual(entity1.id, 'id2')

        d2 = entity1.diff(entity2)

        self.assertEqual(len(d2), 0)

        entity2.apply_diff(d, reverse=True)
        self.assertEqual(entity2.id, 'id1')

    def test_apply_diff_id_ignore(self):
        entity1 = silme.core.Entity('id1')
        entity2 = silme.core.Entity('id2')
        entity3 = silme.core.Entity('id3')
        d = entity1.diff(entity2)

        entity3.apply_diff(d, ignore_mismatch=True)
        self.assertEqual(entity3.id, 'id2')

    def test_diff_multiple(self):
        entity1 = silme.core.Entity('id1')
        entity1.value = "Hey Jude"
        entity2 = silme.core.Entity('id2')
        entity2.value = "Hey Joe"
        entity3 = silme.core.Entity('id3')
        entity3.value = "Hey Jolie"
        d = entity1.diff((entity2, entity3))

        entity1.apply_diff(d)
        self.assertEqual(entity2.id, 'id2')

        entity1.apply_diff(d, reverse=True)
        self.assertEqual(entity1.id, 'id1')

        entity3.apply_diff(d, source=2, result=1)
        self.assertEqual(entity3.id, 'id2')

        entity3.apply_diff(d, source=1, result=0)
        self.assertEqual(entity3.id, 'id1')

        entity3.apply_diff(d, reverse=True, source=2, result=0)
        self.assertEqual(entity3.id, 'id3')

if __name__ == '__main__':
    unittest.main()
