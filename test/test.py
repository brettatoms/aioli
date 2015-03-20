import asyncio
from itertools import filterfalse

import aioli

is_even = lambda x: x % 2 == 0

def test_map_no_coroutine():
    func = lambda x: x
    iterable = list(range(0, 5))
    for index, value in enumerate(aioli.map(func, iterable)):
        assert index == value

def test_map_with_coroutine():
    func = asyncio.coroutine(lambda x: x)
    iterable = list(range(0, 5))
    for index, value in enumerate(aioli.map(func, iterable)):
        assert index == value

def test_filter():
    iterable = list(range(0, 10))
    assert list(filter(is_even, iterable)) == list(aioli.filter(is_even, iterable))

def test_filterfalse():
    iterable = list(range(0, 10))
    assert list(filterfalse(is_even, iterable)) == list(aioli.filterfalse(is_even, iterable))

def test_parallel():
    iterable = list(range(0, 10))
    inc = lambda x: x + 1
    results = set(aioli.parallel(inc, iterable))
    assert len(results) > 0
    assert results == set(map(inc, iterable))
