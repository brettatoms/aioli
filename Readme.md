# Aioli

**Aioli (ayo-OH-lee)** is a little sauce on top of Python's asyncio package.  With a
little **aioli** it makes it easier to take advantage of asyncio in synchronous code.

These helpers are intended for IO bound tasks that yield.  If you're not
yield'ing or if your code is CPU bound then **aioli** probably won't help you
much unless you start getting fancy with passing in your own loops in with their
own executors.

### Await

The `aioli.await()` function calls a coroutine and blocks until it returns. With
`aioli.await()` it's easier to call an asynchrounous coroutine from synchronous
code.

```python
@asyncio.coroutine
def func(x):
    yield from asyncio.sleep(random())
    return x

result = aioli.await(func(1))
```

### Map

The `aioli.map()` functions applies the coroutine to every item of iterable. The
results are yielded as they are available and in the same sort order as the
iterable.

```python
@asyncio.coroutine
def func(x):
    yield from asyncio.sleep(random())
    return x

for result in aioli.map(func, iterable):
    print(result)
```

### Parallel

The `aioli.parallel()` function applies the coroutine to every item of an
iterable.  The difference with `aioli.parallel()` and `aioli.map()` is that the
results are returned as they are available rather than in order.

```python
@asyncio.coroutine
def inc(x):
    yield from asyncio.sleep(random())
    return x + 1

for result in aioli.parallel(func, iterable):
    print(result)
```

### Filter

The `aiolo.filter()` function applies an asynchronous coroutine to an iterable
and yields the results where the coroutine returns `True`.  The results are
yielded in same order as the iterable.

```python

is_even = lambda x: x % 2 == 0
for result in aioli.map(is_even, range(0, 100)):
    print(result)
```

### Filter false

The `aioli.filterfalse()` function is the same as `aioli.filter()` but returns those elements
where the coroutine return `False`.

```python
is_even = lambda x: x % 2 == 0
for result in aioli.map(is_even, range(0, 100)):
    print(result)
```
