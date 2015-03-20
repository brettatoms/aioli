# Aioli

Aioli (ayo-OH-lee) is a little sauce on top of Python's asyncio package.  With a
little aioli it makes it easier to take advantage of asyncio in synchronous code.

```python
# func will be run asynchronously for each item in iterable and results
# will be returned in order as their available
for result in aioli.map(func, iterable):
    print(result)
```
