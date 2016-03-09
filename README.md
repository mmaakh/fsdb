Introduction
============

This is a Python module that implements a key-value store with the following
properties:

  * **RAM efficient:** only queried key value is returned to RAM. The reset
    of the values are stored on disk.

  * **Scalable search time**: if `f` is set to a uniformly distributed hash
    function, then the key values are indexed by a balanced multi-way
    decision tree. I.e. the asymptotic worst run-time time complexity to
    search and find a key value is `O(log n)` when collision-free, where `n`
    is the total number of stored key-value pairs. When collisions
    are accounted for, then the asymptotic worst run time complexity of the
    same is `O(n)`. However, the probability of
    collisions are _extremely_ marginal; for example if a 256bit uniformly
    distributed hash function is used (e.g. SHA256), and if `n=4.8*10^37`,
    then the probability of any collision to occur is `0.01`.

  * **Few dependencies:** the only dependency is Python.

  * **Compatibility:** both Python 2.x and 3.x are supported.

  * **Open source:** licensed under the terms of GPLv3.

Usage
=====
  1. A storage object `mystore` must be instantiated from the class
     `fsdb.storage` as follows: `mystore = fsdb.storage(root=PATH, f=HFUNC, dirlen=LEN,
     v=BOOL)`, where `PATH` is the root directory of storing the indexed
     key-value pairs, `HFUNC` is a function that takes as input a key and
     returns as output a hash of type `str`, `LEN` is maximum directory name
     length (default is 2), and `BOOL` is either `True` or `False` (default is
     `False`).

  2. Then the key-value pairs can be stored, retrieved and deleted by
     `mystore.store(KEY, VALUE)`, `mystore.retrieve(KEY)` and
     `mystore.delete(KEY)`, respectively, where `KEY` must be named such that
     it is a valid file name, and `VALUE` can be any arbitrary value that is to
     be stored.

Example
=======
```python
# import fsdb module
import fsdb
import hashlib

# define your hash function, here we use MD5
def myhash(key):
    return hashlib.md5(key.encode('utf8')).hexdigest()

# instantiate a storage object
mydb = fsdb.storage('./storage_root', f=myhash)


# store some key-value pairs
mydb.store('testkey1', 'testvalue1')
mydb.store('testkey2', 'testvalue2')

# retrieve some key-value pair
myvalue = mydb.retrieve('testkey1')
print(myvalue)

# delete some key-value pair
mydb.delete('testkey1')

# try retrieving the deleted key-value pair
myvalue = mydb.retrieve('testkey1')
if myvalue == None:
    print('deleted')
else:
    print('not deleted')
```
