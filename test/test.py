import asyncio
import aioli

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
