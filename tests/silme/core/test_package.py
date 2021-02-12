import random
import unittest
import sys

import silme.core

class EntityTestCase(unittest.TestCase):

    def setUp(self):
        self.l10npackage = silme.core.Package('test')

    def test_id(self):
        self.assertEqual(self.l10npackage.id, 'test')

    def test_add_structure(self):
        l10nobject = silme.core.Structure('foo')
        self.l10npackage.add_structure(l10nobject)
        self.assertEqual(len(self.l10npackage.structures()), 1)

    def test_add_structure2(self):
        l10nobject = silme.core.Structure('foo')
        self.l10npackage.add_structure(l10nobject, 'test2/test3')
        self.assertEqual(len(self.l10npackage.packages()), 1)
        self.assertEqual(self.l10npackage.packages()[0].id, 'test2')
        self.assertEqual(self.l10npackage.packages()[0].packages()[0].id, 'test3')
        self.assertEqual(self.l10npackage.packages()[0].packages()[0].structure('foo').id, 'foo')

    def test_add_package(self):
        l10npack = silme.core.Package('foo')
        self.l10npackage.add_package(l10npack)
        self.assertEqual(len(self.l10npackage.packages()), 1)

    def test_add_package2(self):
        l10npack = silme.core.Package('foo')
        self.l10npackage.add_package(l10npack, 'test2/test3')
        self.assertEqual(len(self.l10npackage.packages()), 1)
        self.assertEqual(self.l10npackage.packages()[0].id, 'test2')
        self.assertEqual(self.l10npackage.packages()[0].packages()[0].id, 'test3')
        self.assertEqual(self.l10npackage.packages()[0].packages()[0].package('foo').id, 'foo')

    def test_get_objects(self):
        self.l10npackage.add_structure(silme.core.Structure('foo'))
        self.l10npackage.add_structure(silme.core.Structure('foo2'))
        self.l10npackage.add_structure(silme.core.Structure('foo3'))
        self.assertEqual(self.l10npackage.structures()[0].id, 'foo')
        self.assertEqual(self.l10npackage.structures()[1].id, 'foo2')
        self.assertEqual(self.l10npackage.structures()[2].id, 'foo3')

    def test_get_objects2(self):
        self.l10npackage.add_structure(silme.core.Structure('foo'))
        self.l10npackage.add_structure(silme.core.Structure('foo2'))
        self.l10npackage.add_structure(silme.core.Structure('foo3'))
        self.assertEqual(self.l10npackage.structures(ids=True), ['foo', 'foo2', 'foo3'])


    def test_get_packages(self):
        self.l10npackage.add_package(silme.core.Package('foo'))
        self.l10npackage.add_package(silme.core.Package('foo2'))
        self.l10npackage.add_package(silme.core.Package('foo3'))
        self.assertEqual(self.l10npackage.packages()[0].id, 'foo')
        self.assertEqual(self.l10npackage.packages()[1].id, 'foo2')
        self.assertEqual(self.l10npackage.packages()[2].id, 'foo3')

    def test_get_packages2(self):
        self.l10npackage.add_package(silme.core.Package('foo'))
        self.l10npackage.add_package(silme.core.Package('foo2'))
        self.l10npackage.add_package(silme.core.Package('foo3'))
        self.assertEqual(self.l10npackage.packages(ids=True), ['foo', 'foo2', 'foo3'])

    def test_get_entities(self):
        l10nobject = silme.core.Structure('foo')
        l10nobject.add_entity(silme.core.Entity('entid'))
        l10nobject2 = silme.core.Structure('foo2')
        l10nobject2.add_entity(silme.core.Entity('entid2'))
        self.l10npackage.add_structure(l10nobject)
        self.l10npackage.add_structure(l10nobject2)
        entities = self.l10npackage.entities()
        self.assertEqual(len(entities), 2)

    def test_get_entities2(self):
        l10nobject = silme.core.Structure('foo')
        l10nobject.add_entity(silme.core.Entity('entid'))
        l10nobject2 = silme.core.Structure('foo2')
        l10nobject.add_entity(silme.core.Entity('entid2'))
        l10npack = silme.core.Package('test2')
        l10npack.add_structure(l10nobject)
        l10npack.add_structure(l10nobject2)
        self.l10npackage.add_package(l10npack)
        entities = self.l10npackage.entities(recursive=True)
        self.assertEqual(len(entities), 2)
        entities = self.l10npackage.entities(recursive=False)
        self.assertEqual(len(entities), 0)

    def test_get_entities_with_path(self):
        l10nobject = silme.core.Structure('foo')
        l10nobject.add_entity(silme.core.Entity('entid'))
        l10nobject2 = silme.core.Structure('foo2')
        l10nobject.add_entity(silme.core.Entity('entid2'))
        l10npack = silme.core.Package('test2')
        l10npack.add_structure(l10nobject)
        l10npack.add_structure(l10nobject2)
        self.l10npackage.add_package(l10npack)
        entities = self.l10npackage.entities(recursive=True, path=True)
        self.assertEqual(entities[0][1], 'test2/foo')
        entities = self.l10npackage.package('test2').entities(recursive=True, path=True)
        self.assertEqual(entities[0][1], 'foo')

    def test_package_lazy_by_default(self):
        self.assertEqual(self.l10npackage.lazy, True)

    def test_package__stub_exceptions_if_not_lazy(self):
        pack = silme.core.Package('id1', lazy=False)
        self.assertRaises(Exception, pack.add_package_stub,
                                     'id1',
                                     lambda x:silme.core.Package('test1'))
        self.assertRaises(Exception, pack.add_structure_stub,
                                     'id1',
                                     lambda x:silme.core.Structure('id1'))

    def test_package_add_structure_stub(self):
        def resolver(id):
            return silme.core.Structure(id)
        pack = silme.core.Package('id1', lazy=True)
        pack.add_structure_stub('id1', resolver)
        self.assertEqual(len(pack), 1)
        self.assertEqual('id1' in pack, True)
        self.assertEqual(len(pack.structures(ids=True)), 1)
        self.assertEqual(len(pack._structures._stubs), 1)
        self.assertEqual(pack.has_structure('id1'), True)
        self.assertEqual(pack.structure('id1').id, 'id1')
        self.assertEqual(len(pack._structures._stubs), 0)

    def test_package_add_package_stub(self):
        def resolver(id):
            return silme.core.Package(id)
        pack = silme.core.Package('id1', lazy=True)
        pack.add_package_stub('id1', resolver)
        self.assertEqual(len(pack), 1)
        self.assertEqual('id1' in pack, True)
        self.assertEqual(len(pack.packages(ids=True)), 1)
        self.assertEqual(len(pack._packages._stubs), 1)
        self.assertEqual(pack.has_package('id1'), True)
        self.assertEqual(pack.package('id1').id, 'id1')
        self.assertEqual(len(pack._packages._stubs), 0)
