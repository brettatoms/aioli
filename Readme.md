# Aioli

**Aioli (ayo-OH-lee)** is a little sauce on top of Python's asyncio package.  With a
little **aioli** it makes it easier to take advantage of asyncio in synchronous code.

These helpers are intended for IO bound tasks.  If your code is CPU bound then
**aioli** probably won't help you much unless you start getting fancy with
passing in your own loops in with their own executors.

### Map
```python
# Func will be run asynchronously for each item in iterable and results
# will be returned in order as their available.
for result in aioli.map(func, iterable):
    print(result)
```

### Parallel
```python
# Func will be run asynchronously for each item in iterable and results
# will be returned as they are available.  Order is not guaranteed.
inc = lambda x: x + 1
for result in aioli.parallel(func, iterable):
    print(result)
```

### Filter
```python
# Func will be run asynchronously for each item in iterable and results
# will be returned in order as their available.
is_even = lambda x: x % 2 == 0
for result in aioli.map(is_even, range(0, 100)):
print(result)
```

### Filter false
```python
# Func will be run asynchronously for each item in iterable and results
# will be returned in order as their available.
is_even = lambda x: x % 2 == 0
for result in aioli.map(is_even, range(0, 100)):
    print(result)
```
