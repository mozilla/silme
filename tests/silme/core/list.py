import random
import unittest
import sys
sys.path.append('./lib')

import silme.core

class EntityTestCase(unittest.TestCase):

    def setUp(self):
        self.entity_list = silme.core.EntityList('test')

    def test_init1(self):
        self.assertEqual(self.entity_list.id, 'test')

    def test_init2(self):
        self.assertRaises(AttributeError, silme.core.EntityList, 'test', 'foo')

    def test_init3(self):
        entity1 = silme.core.Entity('x')
        entity2 = silme.core.Entity('y')
        self.entity_list = silme.core.EntityList('test', entity1, entity2)
        self.assertEquals(self.entity_list['x'], entity1)
        self.assertEquals(self.entity_list['y'], entity2)

    def test_init4(self):
        entity1 = silme.core.Entity('x')
        entity2 = silme.core.Entity('y')
        entity_list = silme.core.EntityList('test', entity1, entity2)
        self.entity_list = silme.core.EntityList('id2', entity_list)
        self.assertEquals(self.entity_list['x'], entity1)
        self.assertEquals(self.entity_list['y'], entity2)
    
    def test_has_entity1(self):
        entity1 = silme.core.Entity('x')
        self.entity_list.add(entity1)
        self.assertEquals('x' in self.entity_list, True)

    def test_get_entities1(self):
        entity1 = silme.core.Entity('x')
        entity2 = silme.core.Entity('y')
        self.entity_list.add(entity1)
        self.entity_list.add(entity2)
        l = self.entity_list.entities()
        self.failUnless(l[0].id in ('x', 'y'))
        self.failUnless(l[1].id in ('x', 'y'))
        self.assertNotEqual(l[0].id, l[1].id)

    def test_iter_entities(self):
        entity1 = silme.core.Entity('x')
        entity2 = silme.core.Entity('y')
        entity3 = silme.core.Entity('z')
        self.entity_list.add(entity1)
        self.entity_list.add(entity2)
        self.entity_list.add(entity3)
        for id in self.entity_list:
            self.failUnless(id in ('x','y','z'))

    def test_entity_ids1(self):
        entity1 = silme.core.Entity('x')
        entity2 = silme.core.Entity('y')
        self.entity_list.add(entity1)
        self.entity_list.add(entity2)
        ids = self.entity_list.keys()
        self.assertEqual('x' in ids, True)
        self.assertEqual('y' in ids, True)
    
    def test_modify_entity1(self):
        entity1 = silme.core.Entity('x')
        self.entity_list.add(entity1)
        self.entity_list.modify('x', 'test2')
        self.assertEqual(self.entity_list['x'].value, 'test2')

    def test_modify_entity2(self):
        entity1 = silme.core.Entity('x', 'foo')
        entity1.set_value('heh')
        self.entity_list.add(entity1)
        self.entity_list.modify('x', 'test2')
        self.assertEqual(self.entity_list['x'].get_value(), 'test2')

    def test_entity1(self):
        entity1 = silme.core.Entity('x', 'foo')
        self.entity_list.add(entity1)
        self.assertEqual(self.entity_list['x'], entity1)

    def test_get_value(self):
        entity1 = silme.core.Entity('x')
        entity1.set_value('test')
        self.entity_list.add(entity1)
        self.assertEqual(self.entity_list.value('x'), 'test')

    def test_ordered_list(self):
        self.entity_list = silme.core.EntityList('test', ordered=True)
        ids = ('id1', 'id2', 'id3')
        for i in ids:
            self.entity_list.add(silme.core.Entity(i))
        n = 0
        for i in self.entity_list.keys():
            self.assertEqual(i, ids[n])
            n+=1
        n = 0
        for i in self.entity_list:
            self.assertEqual(i, ids[n])
            n+=1

    def test_lazy_list(self):
        self.entity_list = silme.core.EntityList('test', lazy=True)

        def resolve(key, value):
            return silme.core.Entity(key, value)

        self.entity_list.set_stub('id1', resolve, 'Foo1')
        self.assertTrue(len(self.entity_list._stubs), 1)
        self.assertTrue(self.entity_list._stubs, set('id1'))
        e = self.entity_list['id1']
        self.assertEqual(e.id, 'id1')
        self.assertEqual(e.value, 'Foo1')
        self.assertEqual(len(self.entity_list._stubs), 0)

    def test_value_list1(self):
        vlist = silme.core.list.ValueList('test')
        vlist.add(silme.core.Entity('id1', 'Foo1'))
        self.assertEqual(vlist['id1'], 'Foo1')

    def test_value_list2(self):
        vlist = silme.core.list.ValueList('test')
        vlist.add(silme.core.Entity('id1', 'Foo1'))
        self.assertRaises(TypeError, vlist.entities)

if __name__ == '__main__':
    unittest.main()
