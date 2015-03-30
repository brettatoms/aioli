# -*- coding: utf-8 -*-

import asyncio
from itertools import tee

def map(func, iterable, loop=None):
    """Apply function to every item of iterable.

    The functions are run asynchrounousy but the results are returned in order
    as they are available.

    """
    if loop is None:
        loop = asyncio.get_event_loop()

    if not asyncio.iscoroutine(func):
        func = asyncio.coroutine(func)

    # the tasks are added here but nothing starts running until we call
    # loop.run_until_complete()
    tasks = [asyncio.async(func(arg), loop=loop) for arg in iterable]

    for task in tasks:
        # "yield from" would yield each of the results individually if the task
        # return a gathered task
        yield await(task, loop=loop)


def parallel(func, iterable, timeout=None, loop=None):
    """Apply function to every item of iterable.

    Similar to map() but the results are yielded as they are available and the
    order is not guaranteed.

    """
    #
    if loop is None:
        loop = asyncio.get_event_loop()

    if not asyncio.iscoroutine(func):
        func = asyncio.coroutine(func)

    # the tasks are added here but nothing starts running until we call
    # loop.run_until_complete()
    tasks = [asyncio.async(func(arg), loop=loop) for arg in iterable]
    while len(tasks) > 0:
        waiting = asyncio.wait(tasks, loop=loop, timeout=timeout,
                               return_when=asyncio.FIRST_COMPLETED)
        done, pending = loop.run_until_complete(waiting)
        for d in done:
            yield d.result()
        tasks = pending


def reduce():
    pass

def await(coro, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()

    if not asyncio.iscoroutine(coro) and not isinstance(coro, asyncio.Future):
        raise ValueError("requires a coroutine or Task")

    # if coro is a coroutine rather than a task then run_until_completed()
    # automatically wraps it with asyncion.async()
    return loop.run_until_complete(coro)


def any():
    pass


def all():
    pass

def first(func, iterable, loop=None):
    """Return the first element that returns"""
    return next(parallel(func, iterable, loop))


def filter(func, iterable, loop=None):
    """Apply the iterable items to func and yield those that return True.
    """
    iter1, iter2 = tee(iterable)
    for item, result in zip(iter1, map(func, iter2, loop)):
        if result is True:
            yield item


def filterfalse(func, iterable, loop=None):
    """Apply the iterable items to func and yield those that return False.
    """
    iter1, iter2 = tee(iterable)
    for item, result in zip(iter1, map(func, iter2, loop)):
        if result is False:
            yield item
