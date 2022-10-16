import unittest
from io import StringIO
from collections import deque
from main import LRUCache, filter_file


class MainTest(unittest.TestCase):

    def test_lru_cache(self):
        t_cache = LRUCache(2)
        t_cache.set('key1', 'value1')
        t_cache.set('key2', 'value2')
        self.assertEqual(t_cache.queue, deque(['key1', 'key2']))
        t_cache.set('key1', 'value3')
        self.assertEqual(t_cache.queue, deque(['key2', 'key1']))
        t_cache.set('key3', 'value3')
        self.assertEqual(t_cache.queue, deque(['key1', 'key3']))
        with self.assertRaises(KeyError):
            t_cache.Cache_dict['key2']

    def test_filter_func(self):
        text = 'Шла Саша\nПо шоссе\nИ сосала\nСушку\n'
        key_words = ['саша', 'по', 'СУШКУ']
        with StringIO(text) as file:
            gen = filter_file(file, key_words)
            self.assertEqual(next(gen), 'Шла Саша')
            self.assertEqual(next(gen), 'По шоссе')
            self.assertEqual(next(gen), None)
            self.assertEqual(next(gen), 'Сушку')
