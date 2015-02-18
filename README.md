# pystruct
Some useful python data structures

## zdict
ZDict is a python dictionary that can be compressed and uncompressed at will to save space.
It's particularly useful to store a JSONable data structure which needs to be
written rarely and accessed more frequently (logs, stats, etc).

```python
>>> from zdict import ZDict

>>> zd = ZDict({"name": "John", "last_name": "Smith", "numbers": ["(415)-555-5555", "(415)-777-7777"]})
>>> zd.compress()
>>> zd.compressed
True
>>> print str(zd)
{u'last_name': u'Smith', u'name': u'Dave', u'numbers': [u'(415)-555-5555', u'(415)-777-7777']}
>>> zd.decompress()
{u'last_name': u'Smith', u'name': u'Dave', u'numbers': [u'(415)-555-5555', u'(415)-777-7777']}
>>> zd.compressed
False
```

Operations on the compressed dictionary seamlessly decompress and compress it.
```python
>>> zd.compress()
>>> zd['name'] = 'Dave'
>>> print zd
{u'last_name': u'Smith', u'name': u'Dave', u'numbers': [u'(415)-555-5555', u'(415)-777-7777']}
```

Of course this comes at a (CPU) cost, so the best strategy is to perform write operation when the dict is not compressed and then compress it.

You can use the ZDict as a context manager to execute a batch of operations on a it.
```python
with zd as data:
    data['age'] = 28
	data['numbers'].append('(415)-888-8888')
	data['age'] -= 2
```
The ZDict automatically decompress the content (if compressed), assignes it to *data* and compresses it again if it was compressed.

