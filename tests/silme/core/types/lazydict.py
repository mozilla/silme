import unittest
import sys

from silme.core.types.lazydict import LazyDict

class LazyDictTestCase(unittest.TestCase):
    def test_constructor(self):
        # calling built-in types without argument must return empty
        self.assertEqual(LazyDict(), {})
        self.assertIsNot(LazyDict(), {})

    def test_bool(self):
        self.assertIs(not LazyDict(), True)
        self.assertTrue(LazyDict({1: 2}))
        self.assertIs(bool(LazyDict()), False)
        self.assertIs(bool(LazyDict({1: 2})), True)

    def test_keys(self):
        d = LazyDict()
        self.assertEqual(set(d.keys()), set())
        d = LazyDict({'a': 1, 'b': 2})
        k = d.keys()
        self.assertTrue('a' in d)
        self.assertTrue('b' in d)
        self.assertEqual(set(k), {'a','b'})

        self.assertRaises(TypeError, d.keys, None)

    def test_values(self):
        d = LazyDict()
        self.assertEqual(set(d.values()), set())
        d = LazyDict({1:2})
        self.assertEqual(set(d.values()), {2})
        self.assertRaises(TypeError, d.values, None)
        #self.assertEqual(repr(dict(a=1).values()), "dict_values([1])")

    def test_items(self):
        d = LazyDict()
        self.assertEqual(set(d.items()), set())

        d = LazyDict({1:2})
        self.assertEqual(set(d.items()), {(1, 2)})

        self.assertRaises(TypeError, d.items, None)

    def test_contains(self):
        d = LazyDict()
        self.assertNotIn('a', d)
        self.assertFalse('a' in d)
        self.assertTrue('a' not in d)
        d = LazyDict({'a': 1, 'b': 2})
        self.assertIn('a', d)
        self.assertIn('b', d)
        self.assertNotIn('c', d)

        self.assertRaises(TypeError, d.__contains__)

    def test_len(self):
        d = LazyDict()
        self.assertEqual(len(d), 0)
        d = LazyDict({'a': 1, 'b': 2})
        self.assertEqual(len(d), 2)

    def test_getitem(self):
        d = LazyDict({'a': 1, 'b': 2})
        self.assertEqual(d['a'], 1)
        self.assertEqual(d['b'], 2)
        d['c'] = 3
        d['a'] = 4
        self.assertEqual(d['c'], 3)
        self.assertEqual(d['a'], 4)
        del d['b']
        self.assertEqual(d, {'a': 4, 'c': 3})

        self.assertRaises(TypeError, d.__getitem__)

        class BadEq(object):
            def __eq__(self, other):
                raise Exc()
            def __hash__(self):
                return 24

        d = LazyDict()
        d[BadEq()] = 42
        self.assertRaises(KeyError, d.__getitem__, 23)

        class Exc(Exception): pass

        class BadHash(object):
            fail = False
            def __hash__(self):
                if self.fail:
                    raise Exc()
                else:
                    return 42

        x = BadHash()
        d[x] = 42
        x.fail = True
        self.assertRaises(Exc, d.__getitem__, x)

    def test_clear(self):
        d = LazyDict({1:1, 2:2, 3:3})
        d.clear()
        self.assertEqual(d, {})

        self.assertRaises(TypeError, d.clear, None)

    def test_update(self):
        d = LazyDict()
        d.update({1:100})
        d.update({2:20})
        d.update({1:1, 2:2, 3:3})
        self.assertEqual(d, {1:1, 2:2, 3:3})

        d.update()
        self.assertEqual(d, {1:1, 2:2, 3:3})

        self.assertRaises((TypeError, AttributeError), d.update, None)

        class SimpleUserDict:
            def __init__(self):
                self.d = {1:1, 2:2, 3:3}
            def keys(self):
                return self.d.keys()
            def __getitem__(self, i):
                return self.d[i]
        d.clear()
        d.update(SimpleUserDict())
        self.assertEqual(d, {1:1, 2:2, 3:3})

        class Exc(Exception): pass

        d.clear()
        class FailingUserDict:
            def keys(self):
                raise Exc
        self.assertRaises(Exc, d.update, FailingUserDict())

        class FailingUserDict:
            def keys(self):
                class BogonIter:
                    def __init__(self):
                        self.i = 1
                    def __iter__(self):
                        return self
                    def __next__(self):
                        if self.i:
                            self.i = 0
                            return 'a'
                        raise Exc
                    next = __next__
                return BogonIter()
            def __getitem__(self, key):
                return key
        self.assertRaises(Exc, d.update, FailingUserDict())

        class FailingUserDict:
            def keys(self):
                class BogonIter:
                    def __init__(self):
                        self.i = ord('a')
                    def __iter__(self):
                        return self
                    def __next__(self):
                        if self.i <= ord('z'):
                            rtn = chr(self.i)
                            self.i += 1
                            return rtn
                        raise StopIteration
                    next = __next__
                return BogonIter()
            def __getitem__(self, key):
                raise Exc
        self.assertRaises(Exc, d.update, FailingUserDict())

        class badseq(object):
            def __iter__(self):
                return self
            def __next__(self):
                raise Exc()
            next = __next__

        self.assertRaises(Exc, {}.update, badseq())

        self.assertRaises(ValueError, {}.update, [(1, 2, 3)])

    def test_fromkeys(self):
        self.assertEqual(LazyDict().fromkeys('abc'), {'a':None, 'b':None, 'c':None})
        d = LazyDict()
        self.assertIsNot(d.fromkeys('abc'), d)
        self.assertEqual(d.fromkeys('abc'), LazyDict({'a':None, 'b':None, 'c':None}))
        self.assertEqual(d.fromkeys((4,5),0), LazyDict({4:0, 5:0}))
        self.assertEqual(d.fromkeys([]), LazyDict())
        def g():
            yield 1
        self.assertEqual(d.fromkeys(g()), LazyDict({1:None}))
        self.assertRaises(TypeError, {}.fromkeys, 3)
        class dictlike(LazyDict): pass
        self.assertEqual(dictlike.fromkeys('a'), LazyDict({'a':None}))
        self.assertEqual(dictlike().fromkeys('a'), LazyDict({'a':None}))
        self.assertTrue(type(dictlike.fromkeys('a')) is dictlike)
        self.assertTrue(type(dictlike().fromkeys('a')) is dictlike)
        class mydict(LazyDict):
            def __new__(cls):
                return LazyDict()
        ud = mydict.fromkeys('ab')
        self.assertEqual(ud, LazyDict({'a':None, 'b':None}))
        self.assertTrue(isinstance(ud, LazyDict))
        self.assertRaises(TypeError, dict.fromkeys)

        class Exc(Exception): pass

        class baddict1(LazyDict):
            def __init__(self):
                raise Exc()

        self.assertRaises(Exc, baddict1.fromkeys, [1])

        class baddict2(LazyDict):
            def __setitem__(self, key, value):
                raise Exc()

        self.assertRaises(Exc, baddict2.fromkeys, [1])

        # test fast path for dictionary inputs
        d = LazyDict(zip(range(6), range(6)))
        self.assertEqual(LazyDict.fromkeys(d, 0), LazyDict(zip(range(6), [0]*6)))

    def test_copy(self):
        d = LazyDict({1:1, 2:2, 3:3})
        self.assertEqual(d.copy(), LazyDict({1:1, 2:2, 3:3}))
        self.assertEqual(LazyDict().copy(), LazyDict())
        self.assertRaises(TypeError, d.copy, None)

    def test_get(self):
        d = LazyDict()
        self.assertIs(d.get('c'), None)
        self.assertEqual(d.get('c', 3), 3)
        d = LazyDict({'a': 1, 'b': 2})
        self.assertIs(d.get('c'), None)
        self.assertEqual(d.get('c', 3), 3)
        self.assertEqual(d.get('a'), 1)
        self.assertEqual(d.get('a', 3), 1)
        self.assertRaises(TypeError, d.get)
        self.assertRaises(TypeError, d.get, None, None, None)

    def test_setdefault(self):
        # dict.setdefault()
        d = LazyDict()
        self.assertIs(d.setdefault('key0'), None)
        d.setdefault('key0', [])
        self.assertIs(d.setdefault('key0'), None)
        d.setdefault('key', []).append(3)
        self.assertEqual(d['key'][0], 3)
        d.setdefault('key', []).append(4)
        self.assertEqual(len(d['key']), 2)
        self.assertRaises(TypeError, d.setdefault)

        class Exc(Exception): pass

        class BadHash(object):
            fail = False
            def __hash__(self):
                if self.fail:
                    raise Exc()
                else:
                    return 42

        x = BadHash()
        d[x] = 42
        x.fail = True
        self.assertRaises(Exc, d.setdefault, x, [])

    def test_popitem(self):
        # dict.popitem()
        for copymode in -1, +1:
            # -1: b has same structure as a
            # +1: b is a.copy()
            for log2size in range(12):
                size = 2**log2size
                a = LazyDict()
                b = LazyDict()
                for i in range(size):
                    a[repr(i)] = i
                    if copymode < 0:
                        b[repr(i)] = i
                if copymode > 0:
                    b = a.copy()
                for i in range(size):
                    ka, va = ta = a.popitem()
                    self.assertEqual(va, int(ka))
                    kb, vb = tb = b.popitem()
                    self.assertEqual(vb, int(kb))
                    self.assertFalse(copymode < 0 and ta != tb)
                self.assertFalse(a)
                self.assertFalse(b)

        d = LazyDict()
        self.assertRaises(KeyError, d.popitem)

    def test_pop(self):
        # Tests for pop with specified key
        d = LazyDict()
        k, v = 'abc', 'def'
        d[k] = v
        self.assertRaises(KeyError, d.pop, 'ghi')

        self.assertEqual(d.pop(k), v)
        self.assertEqual(len(d), 0)

        self.assertRaises(KeyError, d.pop, k)

        # verify longs/ints get same value when key > 32 bits
        # (for 64-bit archs).  See SF bug #689659.
        x = 4503599627370496
        y = 4503599627370496
        h = LazyDict({x: 'anything', y: 'something else'})
        self.assertEqual(h[x], h[y])

        self.assertEqual(d.pop(k, v), v)
        d[k] = v
        self.assertEqual(d.pop(k, 1), v)

        self.assertRaises(TypeError, d.pop)

        class Exc(Exception): pass

        class BadHash(object):
            fail = False
            def __hash__(self):
                if self.fail:
                    raise Exc()
                else:
                    return 42

        x = BadHash()
        d[x] = 42
        x.fail = True
        self.assertRaises(Exc, d.pop, x)

    def test_mutatingiteration(self):
        # changing dict size during iteration
        #d = LazyDict()
        #d[1] = 1
        #with self.assertRaises(RuntimeError):
        #    for i in d:
        #        d[i+1] = 1
        pass

    def test_repr(self):
        #d = LazyDict()
        #self.assertEqual(repr(d), 'LazyDict()')
        #d[1] = 2
        #self.assertEqual(repr(d), 'LazyDict(dict_keys([1]))')
        pass

    def test_missing(self):
        self.assertFalse(hasattr(LazyDict, "__missing__"))
        # Test several cases:
        # (D) subclass defines __missing__ method returning a value
        # (E) subclass defines __missing__ method raising RuntimeError
        # (F) subclass sets __missing__ instance variable (no effect)
        # (G) subclass doesn't define __missing__ at a all
        class D(dict):
            def __missing__(self, key):
                return 42
        d = D({1: 2, 3: 4})
        self.assertEqual(d[1], 2)
        self.assertEqual(d[3], 4)
        self.assertTrue(2 not in d)
        self.assertTrue(2 not in d.keys())
        self.assertEqual(d[2], 42)
        class E(dict):
            def __missing__(self, key):
                raise RuntimeError(key)
        e = E()
        try:
            e[42]
        except RuntimeError as err:
            self.assertEqual(err.args, (42,))
        else:
            self.fail("e[42] didn't raise RuntimeError")
        class F(dict):
            def __init__(self):
                # An instance variable __missing__ should have no effect
                self.__missing__ = lambda key: None
        f = F()
        try:
            f[42]
        except KeyError as err:
            self.assertEqual(err.args, (42,))
        else:
            self.fail("f[42] didn't raise KeyError")
        class G(dict):
            pass
        g = G()
        try:
            g[42]
        except KeyError as err:
            self.assertEqual(err.args, (42,))
        else:
            self.fail("g[42] didn't raise KeyError")


    def test_tuple_keyerror(self):
        # SF #1576657
        d = LazyDict()
        try:
            d[(1,)]
        except KeyError as e:
            self.assertEqual(e.args, ((1,),))
        else:
            self.fail("missing KeyError")

    def test_bad_key(self):
        # Dictionary lookups should fail if __cmp__() raises an exception.
        class CustomException(Exception):
            pass

        class BadDictKey:
            def __hash__(self):
                return hash(self.__class__)

            def __cmp__(self, other):
                if isinstance(other, self.__class__):
                    raise CustomException
                return other

        d = LazyDict()
        x1 = BadDictKey()
        x2 = BadDictKey()
        d[x1] = 1
        #for stmt in ['d[x2] = 2',
        #             'z = d[x2]',
        #             'x2 in d',
        #             'x2 in d',
        #             'd.get(x2)',
        #             'd.setdefault(x2, 42)',
        #             'd.pop(x2)',
        #             'd.update({x2: 2})']:
        #    with self.assertRaises(CustomException):
        #        exec stmt in locals()

##########

    def test_lazy_keys(self):
        def resolver(id):
            p = {'b': 2, 'c': 3}
            return p[id]
        d = LazyDict({'a': 1})
        d.set_stub('b', resolver)
        d.set_stub('c', resolver)
        d['d'] = 4
        k = d.keys()
        self.assertTrue('a' in d)
        self.assertTrue('b' in d)
        self.assertTrue('c' in d)
        self.assertTrue('d' in d)
        self.assertEqual(set(k), {'a','b','c','d'})

    def test_lazy_values(self):
        def resolver(id):
            p = {'c': 3}
            return p[id]
        d = LazyDict()
        self.assertEqual(set(d.values()), set())
        d = LazyDict({1:2})
        d.set_stub('c', resolver)
        v = d.values()
        self.assertEqual(set(v), {2,3})

        self.assertRaises(TypeError, d.values, None)

    def test_lazy_items(self):
        d = LazyDict()
        d.set_stub(1, lambda x:x)
        self.assertEqual(set(d.items()), {(1, 1)})

        d = LazyDict({1:2})
        d.set_stub(2, lambda x:x)
        self.assertEqual(set(d.items()), {(1, 2), (2, 2)})

    def test_lazy_contains(self):
        d = LazyDict()
        self.assertNotIn('a', d)
        self.assertFalse('a' in d)
        self.assertTrue('a' not in d)
        d = LazyDict({'a': 1, 'b': 2})
        self.assertIn('a', d)
        self.assertIn('b', d)
        self.assertNotIn('c', d)

        self.assertRaises(TypeError, d.__contains__)

    def test_lazy_len(self):
        d = LazyDict({'1':1})
        self.assertEqual(len(d), 1)
        d['2'] = 2
        self.assertEqual(len(d), 2)
        d.set_stub('3', lambda x: x)
        self.assertEqual(len(d), 3)


    def test_lazy_getitem(self):
        d = LazyDict({'a': 1, 'b': 2})
        self.assertEqual(d['a'], 1)
        self.assertEqual(d['b'], 2)
        d['c'] = 3
        d['a'] = 4
        self.assertEqual(d['c'], 3)
        self.assertEqual(d['a'], 4)
        del d['b']
        self.assertEqual(d, {'a': 4, 'c': 3})

        self.assertRaises(TypeError, d.__getitem__)

        class BadEq(object):
            def __eq__(self, other):
                raise Exc()
            def __hash__(self):
                return 24

        d = LazyDict()
        d[BadEq()] = 42
        self.assertRaises(KeyError, d.__getitem__, 23)

        class Exc(Exception): pass

        class BadHash(object):
            fail = False
            def __hash__(self):
                if self.fail:
                    raise Exc()
                else:
                    return 42

        x = BadHash()
        d[x] = 42
        x.fail = True
        self.assertRaises(Exc, d.__getitem__, x)

    def test_lazy_clear(self):
        d = LazyDict({1:1, 2:2, 3:3})
        d.set_stub(4, lambda x:x)
        d.clear()
        self.assertEqual(d, {})
        self.assertEqual(set(d.keys()), set())
        self.assertEqual(set(d.values()), set())

        self.assertRaises(TypeError, d.clear, None)

    def test_lazy_update(self):
        d = LazyDict()
        d.set_stub(4, lambda x:x)
        d.update(LazyDict({1:100}))
        d.update(LazyDict({2:20}))
        d.update({4:5})
        d.update(LazyDict({1:1, 2:2, 3:3}))
        self.assertEqual(d, {1:1, 2:2, 3:3, 4:5})

        d.update()
        self.assertEqual(d, {1:1, 2:2, 3:3, 4:5})

        self.assertRaises((TypeError, AttributeError), d.update, None)

        class SimpleUserDict:
            def __init__(self):
                self.d = {1:1, 2:2, 3:3}
            def keys(self):
                return self.d.keys()
            def __getitem__(self, i):
                return self.d[i]
        d.clear()
        d.update(SimpleUserDict())
        self.assertEqual(d, {1:1, 2:2, 3:3})

    def test_lazy_copy(self):
        d = LazyDict({'1':1})
        d['2'] = 2
        x = d.copy()
        self.assertEqual(len(x), 2)
        i = {'num': 0}
        def r(key, i):
            i['num'] += 1
            return i['num']
        d.set_stub('3', r, i)
        x = d.copy()
        self.assertEqual(d['3'], 1)
        self.assertEqual(len(d._stubs), 0)
        self.assertEqual(len(x._stubs), 1)
        self.assertEqual(x['3'], 2)
        self.assertEqual(len(x._stubs), 0)
        x = d.copy()
        self.assertEqual(d['3'], 1)
        self.assertEqual(x['3'], 1)

    def test_lazy_get(self):
        d = LazyDict({'a': 1, 'b': 2})
        d.set_stub('d', lambda x:x)
        self.assertIs(d.get('c'), None)
        self.assertEqual(d.get('c', 3), 3)
        self.assertEqual(d.get('a'), 1)
        self.assertEqual(d.get('a', 3), 1)
        self.assertEqual(d.get('d'), 'd')
        self.assertEqual(d.get('d', 3), 'd')
        self.assertRaises(TypeError, d.get)
        self.assertRaises(TypeError, d.get, None, None, None)

    def test_lazy_setdefault(self):
        d = LazyDict()
        self.assertIs(d.setdefault('key0'), None)
        d.set_stub('key0', lambda x:'value0')
        self.assertIs(d.setdefault('key0'), 'value0')
        d.set_stub('key0', lambda x:'value0')
        self.assertEqual(d.setdefault('key1', 'value1'), 'value1')
        self.assertEqual(d['key1'], 'value1')
        self.assertEqual(d.setdefault('key0', 'value2'), 'value0')

    def test_lazy_popitem(self):
        d = LazyDict({1: 1})
        d.set_stub(2, lambda x:x)
        k, v = d.popitem()
        self.assertEqual(k, v)
        k, v = d.popitem()
        self.assertEqual(k, v)
        self.assertEqual(k, 2)
        self.assertEqual(len(d._stubs), 0)
        self.assertRaises(KeyError, d.popitem)

    def test_lazy_pop(self):
        d = LazyDict()
        k, v = ('abc', 'def')
        d.set_stub(k, lambda x:'def')
        self.assertRaises(KeyError, d.pop, 'ghi')

        self.assertEqual(d.pop(k), v)
        self.assertEqual(len(d), 0)

        self.assertRaises(KeyError, d.pop, k)

        self.assertEqual(d.pop(k, v), v)
        d.set_stub(k, lambda x:v)
        self.assertEqual(d.pop(k, 1), v)

        self.assertRaises(TypeError, d.pop)

    def test_lazy_delitem(self):
        d = LazyDict()
        d['1'] = 1
        d['2'] = 2
        del d['1']
        self.assertEqual(len(d), 1)
        self.assertRaises(KeyError, d.__getitem__, '1')
        d.set_stub('1', lambda x:x)
        self.assertEqual(len(d), 2)
        del d['1']
        self.assertEqual(len(d), 1)
        self.assertRaises(KeyError, d.__getitem__, '1')
        d.set_stub('1', lambda x:x)
        self.assertEqual(d['1'], '1')
        del d['1']
        self.assertEqual(len(d), 1)
        self.assertRaises(KeyError, d.__getitem__, '1')
