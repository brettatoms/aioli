# -*- coding: utf-8 -*-

import asyncio

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


def parallel():
    # Run tasks in "parallel" on an asyncio event loop and yielding the results
    # as they come in
    pass
