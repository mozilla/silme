import random
import unittest
import sys
import re
sys.path.append('./lib')

import silme.core

class structureTestCase(unittest.TestCase):

    def setUp(self):
        self.structure = silme.core.Structure('id')

    def test_id(self):
        self.structure.id = 'test'
        self.assertEqual(self.structure.id, 'test')

    def test_add_element(self):
        entity = silme.core.Entity('entid')
        entity2 = silme.core.Entity('entid2')
        self.structure.add_at_pos(entity, 0)
        self.structure.add_at_pos(entity2, 0)
        self.assertEqual(self.structure.get_entity_pos('entid'), 1)
        self.assertEqual(self.structure.get_entity_pos('entid2'), 0)

    def test_add_entity(self):
        entity = silme.core.Entity('entid')
        entity2 = silme.core.Entity('entid2')
        entity3 = silme.core.Entity('entid3')
        entity4 = silme.core.Entity('entid4')
        # make sure add_entity returns 1
        self.assertEqual(self.structure.add_entity(entity), 1) 
        self.structure.add_entity(entity2, 1)
        self.structure.add_entity(entity3, 0)
        self.structure.add_entity(entity4, 1)
        self.assertEqual(self.structure.entity_pos('entid'), 2)
        self.assertEqual(self.structure.entity_pos('entid2'), 3)
        self.assertEqual(self.structure.entity_pos('entid3'), 0)
        self.assertEqual(self.structure.entity_pos('entid4'), 1)

    def test_get_value(self):
        entity = silme.core.Entity('entid')
        entity.set_value('foo')
        self.structure.add_entity(entity)
        self.assertEqual(self.structure.value('entid'), 'foo')


    def test_get_entity(self):
        self.structure.add_entity(silme.core.Entity('entid'))
        self.structure.add_entity(silme.core.Entity('entid2'))
        self.assertEqual(len(self.structure.get_entities()), 2)
        self.assertEqual(self.structure.get_entities()[0].id, 'entid')
        self.assertEqual(self.structure.get_entities()[1].id, 'entid2')

    def test_get_entity_ids(self):
        self.structure.add_entity(silme.core.Entity('entid'))
        self.structure.add_entity(silme.core.Entity('entid2'))
        self.assertEqual(self.structure.ids(), ['entid', 'entid2'])

    def test_has_entity(self):
        self.structure.add_entity(silme.core.Entity('entid'))
        self.structure.add_entity(silme.core.Entity('entid2'))
        self.assertEqual(len(self.structure.entities()), 2)
        self.assertEqual(self.structure.has_entity('entid'), True)
        self.assertEqual(self.structure.has_entity('entid3'), False)

    def test_modify_entity(self):
        entity = silme.core.Entity('entid')
        entity.set_value('testvalue')
        self.structure.add_entity(entity)
        self.assertEqual(self.structure.modify_entity('entid', 'newvalue'), True)
        self.assertEqual(entity.get_value(), 'newvalue')

    def test_modify_entity2(self):
        entity = silme.core.Entity('entid')
        entity.set_value('testvalue')
        self.structure.add_entity(entity)
        self.assertRaises(KeyError, self.structure.modify_entity, 'endid', 'newvalue')

    def test_modify_entity3(self):
        entity = silme.core.Entity('entid')
        entity.default_code = 'pl'
        entity.set_value('testvalue')
        self.structure.add_entity(entity)
        self.structure.modify_entity('entid', 'newvalue')
        self.assertEqual(entity.get_value(), 'newvalue')
    
    def test_get_entity(self):
        entity = silme.core.Entity('entid')
        self.structure.add_entity(entity)
        self.assertEqual(self.structure.entity('entid'), entity)
        self.assertRaises(KeyError, self.structure.entity, 'endid')

    def test_get_entity_pos(self):
        entity = silme.core.Entity('entid')
        self.structure.add_string('foo')
        self.structure.add_entity(silme.core.Entity('entityid2'))
        self.structure.add_string('foo')
        self.structure.add_entity(entity)
        self.structure.add_string('foo')
        self.assertEqual(self.structure.entity_pos('entid'), 3)

    def test_remove_entity(self):
        entity = silme.core.Entity('entid')
        self.structure.add_entity(silme.core.Entity('entityid3'))
        self.structure.add_entity(entity)
        self.structure.add_entity(silme.core.Entity('entityid2'))
        self.assertEqual(self.structure.remove_entity('entid'), True)
        self.assertRaises(KeyError, self.structure.entity, 'endid')
    
    def test_add_element(self):
        entity = silme.core.Entity('entid')
        comment = silme.core.Comment()
        comment.add('foo')
        str = 'foo'
        self.assertEqual(self.structure.add(entity), 1)
        self.assertEqual(self.structure.add(comment), 1)
        self.assertEqual(self.structure.add(str), 1)
        self.assertRaises(Exception, self.structure.add, sys)

    def test_add_elements(self):
        entity = silme.core.Entity('entid')
        comment = silme.core.Comment()
        comment.add('foo')
        str = 'foo'
        list = [entity, comment, entity, str]
        self.assertEqual(self.structure.add_elements(list), 4)

    def test_get_entitylist(self):
        self.structure.add_string('foo')
        self.structure.add_entity(silme.core.Entity('entid'))
        self.structure.add_string('foo')
        self.structure.add_entity(silme.core.Entity('entid2'))
        self.structure.add_string('foo')
        entitylist = self.structure.entitylist()
        self.assertEqual(len(entitylist.entities()), 2)
        self.assertEqual(entitylist['entid'].id, 'entid')
        self.assertEqual(entitylist['entid2'].id, 'entid2')

    def test_process(self):
        def process_entity(entity, subs):
            entity.value = re.sub('\&([^$]+)\;',
                                  lambda m:subs[m.group(1)],
                                  str(entity.value))
        def process(self):
            for elem in self:
                if isinstance(elem, silme.core.Entity):
                    process_entity(elem, self.params['exents'])
        self.structure.set_process_cb(process)
        entity1 = silme.core.Entity('id', 'Test &varMe; it')
        self.structure.params = {}
        self.structure.params['exents'] = {'varMe': 'Woo'}
        self.structure.add_entity(entity1)
        self.structure.process()
        self.assertEqual(self.structure.value('id'), 'Test Woo it')

if __name__ == '__main__':
    unittest.main()
