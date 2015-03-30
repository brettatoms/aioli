import asyncio
from itertools import filterfalse
from random import random

import pytest

import aioli

is_even = lambda x: x % 2 == 0

def test_await_with_func():
    func = lambda x: x
    with pytest.raises(ValueError):
        aioli.await(func(1))

def test_await_with_coroutine():

    @asyncio.coroutine
    def func(x):
        return x
    result = aioli.await(func(1))
    assert result == 1


def test_await_with_task():

    @asyncio.coroutine
    def func(x):
        return x
    task = asyncio.async(func(1))
    result = aioli.await(task)
    assert result == 1


def test_map_no_coroutine():
    func = lambda x: x
    iterable = list(range(0, 5))
    for index, value in enumerate(aioli.map(func, iterable)):
        assert index == value

def test_map_with_coroutine():
    def func(x):
        yield from asyncio.sleep(random())
        return x
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


def test_channel():
    in_queue = asyncio.Queue()
    out_queue = asyncio.Queue()

    @asyncio.coroutine
    def func(in_queue, out_queue):
        data = None
        while True:
            print('get from in_queue')
            data = (yield from in_queue.get())
            # if data is None:
            #     print('yield from chan')
            #     data = (yield)
            #     #data = next(in_chan)
            #     # data = next(in_chan)
            #     print('data: ', data)
            print('data: ', data)
            print('out send')
            yield from out_queue.put(data + 1)
            print('sent')
            yield from None
            #data = (yield data + 1)

    coro = func(in_queue, out_queue)

    for x in range(0, 3):
        print('send: ', x)
        #in_queue.put_nowait(x)
        #aioli.await(asyncio.async(in_queue.put(x)))
        #aioli.await(in_queue.put(x))
        in_queue.put_nowait(x)
        next(coro)
        x = aioli.await(asyncio.async(out_queue.get()))
        aioli.await(coro)
        #x = out_queue.get_nowait()
        print('received: ', x)



def xtest_channel():

    # def channel(func):
    #     def _(*args, **kwargs):
    #         c = aioli.Channel()
    #         kwargs['channel'] = c
    #         return func(*args, **kwargs)
    #     return _

    def channel(name):
        data = None
        while True:
            if data is not None:
                print('{} yield {}'.format(name, data))
                yield data
            print('{} get'.format(name))
            data = (yield)
            print('{} got: {}'.format(name, data))


    @asyncio.coroutine
    def func(in_chan, out_chan):
        #channel => data
        data = None
        while True:
            data = yield (yield from in_chan)
            # if data is None:
            #     print('yield from chan')
            #     data = (yield)
            #     #data = next(in_chan)
            #     # data = next(in_chan)
            #     print('data: ', data)
            print('data: ', data)
            print('out send')
            out_chan.send(data + 1)
            #data = (yield data + 1)


    in_chan = channel('in')
    print('next in_chan')
    next(in_chan)

    out_chan = channel('out')
    print('next out_chan')
    next(out_chan)

    #channel = aioli.Channel()
    coro = func(in_chan, out_chan)
    print('coro: ', coro)
    print('next coro')
    #next(coro)

    for x in range(0, 3):
        print('send: ', x)
        #x = coro.send(x)
        y = in_chan.send(x)
        print('y: ', y)
        next(coro)
        x = next(out_chan)
        print('response: ', x)
        #asyncio.run_until_complete(asyncio.async(coro))

    # for x in range(0, 3):
    #     print('x: ', x)
    #     #aioli.await(channel.send(coro, x))
    #     channel.send(coro, x)
    #     print('sent')
    #     y = aioli.await(channel.receive(coro))
    #     #y = channel.receive(coro)
    #     print('y: ', y)
    #     assert y == x + 1

    raise ValueError()
