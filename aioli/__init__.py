# -*- coding: utf-8 -*-

import asyncio
from itertools import tee

def map(func, iterable, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()

    if not asyncio.iscoroutine(func):
        func = asyncio.coroutine(func)

    tasks = [asyncio.async(func(arg)) for arg in iterable]
    for task in tasks:
        # run until the completion of each task individually and yield as they're ready
        loop.run_until_complete(task)
        # "yield from" would yield each of the results individually if the task
        # return a gathered task
        yield task.result()


def parallel(func, iterable, timeout=None, loop=None):
    # Run tasks in "parallel" on an asyncio event loop and yielding the results
    # as they come in...like map but not in order
    if loop is None:
        loop = asyncio.get_event_loop()

    if not asyncio.iscoroutine(func):
        func = asyncio.coroutine(func)

    tasks = [asyncio.async(func(arg)) for arg in iterable]
    while len(tasks) > 0:
        waiting = asyncio.wait(tasks, loop=loop, timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
        done, pending = loop.run_until_complete(waiting)
        for d in done:
            yield d.result()
        tasks = pending


def reduce():
    pass


def any():
    pass


def all():
    pass


def filter(func, iterable, loop=None):
    iter1, iter2 = tee(iterable)
    for item, result in zip(iter1, map(func, iter2, loop)):
        if result is True:
            yield item

def filterfalse(func, iterable, loop=None):
    iter1, iter2 = tee(iterable)
    for item, result in zip(iter1, map(func, iter2, loop)):
        if result is False:
            yield item
