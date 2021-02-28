import unittest
import sys

from silme.core.entity import Entity, ComplexValue
from collections import OrderedDict

class EntityTestCase(unittest.TestCase):

    def setUp(self):
        self.entity = Entity('test')

    def test_id(self):
        self.assertEqual(self.entity.id, 'test')

    def test_value1(self):
        self.entity.value = 'testvalue'
        self.assertEqual(self.entity.value, 'testvalue')
        self.assertEqual(self.entity.get_value(), self.entity.value)

    def test_value3(self):
        self.entity = Entity('test', 'testvalue')
        self.assertEqual(self.entity.value, 'testvalue')
        self.assertEqual(self.entity.get_value(), self.entity.value)

    def test_value5(self):
        self.assertEqual(self.entity.get_value(), None)

    def test_value6(self):
        self.entity.value = 'foo'
        self.assertEqual(self.entity.value, 'foo')

    def test_list1(self):
        self.entity.value = ['foo','foo2']
        self.assertEqual(self.entity.value, 'foo')

    def test_list2(self):
        self.entity.value = ['foo','foo2']
        self.assertEqual(self.entity[0], 'foo')
        self.assertEqual(self.entity[1], 'foo2')

    def test_list3(self):
        self.entity.value = ['foo','foo2']
        self.assertEqual(self.entity.get_value(0), 'foo')
        self.assertEqual(self.entity.get_value(1), 'foo2')

    def test_list4(self):
        self.entity = Entity('test', ['old','old2'])
        self.entity[0] = 'foo'
        self.entity[1] = 'foo2'
        self.assertEqual(self.entity.get_value(0), 'foo')
        self.assertEqual(self.entity.get_value(1), 'foo2')

    def test_list5(self):
        self.entity.value = ['foo','foo2']
        del self.entity[1]
        self.assertEqual(self.entity.get_value(0), 'foo')
        self.assertRaises(IndexError, self.entity.get_value, 1)

    def test_dict1(self):
        self.entity = Entity('test', {'male':'Foo','female':'Foo2'})
        self.assertTrue(self.entity.value in ('Foo', 'Foo2'))

    def test_dict2(self):
        self.entity.value = {'male':'Foo','female':'Foo2'}
        self.assertTrue(self.entity.value in ('Foo', 'Foo2'))

    def test_dict3(self):
        self.entity.value = {'male':'Foo','female':'Foo2'}
        self.assertTrue(self.entity.get_value() in ('Foo', 'Foo2'))

    def test_dict4(self):
        self.entity.value = {'male':'Foo','female':'Foo2'}
        self.assertEqual(self.entity.get_value('male'), 'Foo')
        self.assertEqual(self.entity.get_value('female'), 'Foo2')

    def test_dict5(self):
        self.entity.value = {'male':'Foo','female':'Foo2'}
        self.assertEqual(self.entity['male'], 'Foo')
        self.assertEqual(self.entity['female'], 'Foo2')

    def test_dict6(self):
        self.entity.value = {'male':'Foo','female':'Foo2'}
        self.entity['male']='Foo3'
        self.assertEqual(self.entity['male'], 'Foo3')
        self.assertEqual(self.entity['female'], 'Foo2')

    def test_dict7(self):
        self.entity.value = {'male':'Foo','female':'Foo2'}
        del self.entity['male']
        self.assertEqual(self.entity['female'], 'Foo2')
        self.assertRaises(KeyError, self.entity.get_value, 'male')


    def test_complex5(self):
        self.entity.value = ComplexValue({'male':'Foo2','female':'Foo3'})
        self.assertEqual(self.entity['male'], 'Foo2')

    def test_complex6(self):
        self.entity.value = ComplexValue(['foo','foo4'])
        self.assertEqual(self.entity[1], 'foo4')

    def test_complex7(self):
        self.entity.value = ComplexValue('Foo')
        self.assertRaises(TypeError, self.entity.__getitem__, 0)

    def test_complex8(self):
        self.entity.value = ComplexValue('Foo')
        self.assertRaises(TypeError, self.entity.__getitem__, 0)
        self.entity.value = ComplexValue(['Foo3','Foo4'])
        self.assertEqual(self.entity[1], 'Foo4')
        self.entity.value = ComplexValue({'one':'Foo5','few':'Foo6','many':'Foo7'})
        self.assertEqual(self.entity['few'], 'Foo6')

    def test_complex9(self):
        self.entity.value = ComplexValue('Foo')
        self.assertEqual(self.entity.value, 'Foo')
        self.entity.value = ComplexValue(['Foo3','Foo4'])
        self.assertEqual(self.entity.value, 'Foo3')
        self.entity.value = ComplexValue(OrderedDict((('one','Foo5'),('few','Foo6'),('many','Foo7'))))
        self.assertEqual(self.entity.value, 'Foo5')

    def test_custom1(self):
        def plural_form(value, n=1):
            return value[0 if n==1 else 1]
        
        
        self.entity._select_value = plural_form
        self.entity.value = ['Firefox', 'Firefoxes']
        self.assertEqual(self.entity.value, 'Firefox')
        self.assertEqual(self.entity.get_value(1), 'Firefox')
        self.assertEqual(self.entity.get_value(5), 'Firefoxes')

    def test_values1(self):
        vals = ['foo', 'foo2']
        self.entity.value = vals
        vals.pop()
        self.assertNotEqual(self.entity.values, vals)
        #x = self.entity.values
        #x.pop()
        #self.assertEqual(x, vals)
        #self.assertNotEqual(self.entity.values, x)
