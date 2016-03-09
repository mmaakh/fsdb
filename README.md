Introduction
============

This is a simple, yet scalable, Python module that implements a key-value store
with the following properties:

  * **RAM efficient:** only the queried key value is stored in RAM. The reset
    of the key values are kept on disk.

  * **Scalable search time**: if `f` is set to a uniformly distributed hash
    function, then the key values are indexed by a balanced multi-way
    decision tree. I.e. the asymptotic worst run-time complexity to
    search and find a key value is `O(log n)` when collision-free, where `n`
    is the total number of stored key-value pairs. When collisions
    are accounted for, then the asymptotic worst run time complexity of the
    same is `O(n)`. However, the probability of
    collisions are _extremely_ marginal; for example if a 256bit uniformly
    distributed hash function is used (e.g. SHA256), and if `n=4.8*10^37`,
    then the probability of any collision to occur is `0.01`. More details on
    the probability of such unlikely collisions can be found [here]
    (https://en.wikipedia.org/wiki/Birthday_attack).

  * **Few dependencies:** the only software dependency is Python.

  * **Compatibility:** both Python 2.x and 3.x are supported.

  * **Open source:** licensed under the terms of GPLv3.

Scope
-----
If you are satisfied with the speed of the read and write operations on your
file system (could be physically on a spinning disk, SSD, or RAM) by using a
Python interpretor, except for wanting the total run-time and RAM
consumption to not increase significantly as you add more key-value pairs, then
this module is a valid choice.

However, if you aren't satisfied with the run-time speed of read/write
operations on your file system, nor that of your Python interpretor, then
this module isn't optimal.

The primary motivation of this module is for a use case of mine where the
constant delays imposed by the file system and Python were sufficient are
adequately fast, except that I did not wish the delay to increase significantly
as the storage gets bigger. Additionally, I have the constraint that RAM is too
precious to store a large key-value store in it, but cheap enough to execute a
Python code.

**Note:** if you really like this key-value store module and wish to stretch to its
limits, you may try setting `root` to a path that physically exists in a RAM
disk, along with attempting to execute your code using PyPy2 or PyPy3. I have
not tried this as of yet, however if you do so then I am interested in knowing
your findings.


A _preliminary_ benchmark
-----------------------
Below is the result of executing `python3.4 preliminary_benchmark.py`, which
tests the speed of computing the md5 hash of keys (for comparision), and
speed of storing, retrieving, deleting and retrieving deleted key-value pairs
by repeating them for 10,000 times. The results are as follows:

```
benchmarking md5.. ok
  md5: 479217.5860335451 operations per second

benchmarking storing key-value pairs.. ok
  store: 7944.541497371237 operations per second

benchmarking retrieving key-value pairs.. ok
  retrieve: 16826.713460314862 operations per second

benchmarking deleting key-value pairs with cleanup.. ok
  delete: 1216.4649856478266 operations per second

preparing for next test.. ok
benchmarking deleting key-value pairs without cleanup.. ok
  delete: 14322.274952723528 operations per second

benchmarking retrieving nonexistent key-value pairs.. ok
  delretrieve: 47092.987875052066 operations per second
```

My `root` is set to point to a file that exists in a RAID10 ZFS partition with
the following parameters (as returned by `zpool get all`):
```
NAME        PROPERTY                    VALUE                       SOURCE
mypool  size                        1.81T                       -
mypool  capacity                    83%                         -
mypool  altroot                     -                           default
mypool  version                     -                           default
mypool  bootfs                      -                           default
mypool  delegation                  on                          default
mypool  autoreplace                 off                         default
mypool  cachefile                   -                           default
mypool  failmode                    wait                        default
mypool  listsnapshots               off                         default
mypool  autoexpand                  off                         default
mypool  dedupditto                  0                           default
mypool  dedupratio                  1.00x                       -
mypool  free                        313G                        -
mypool  allocated                   1.51T                       -
mypool  readonly                    off                         -
mypool  ashift                      0                           default
mypool  comment                     -                           default
mypool  expandsize                  -                           -
mypool  freeing                     0                           default
mypool  fragmentation               30%                         -
mypool  leaked                      0                           default
mypool  feature@async_destroy       enabled                     local
mypool  feature@empty_bpobj         enabled                     local
mypool  feature@lz4_compress        active                      local
mypool  feature@spacemap_histogram  active                      local
mypool  feature@enabled_txg         active                      local
mypool  feature@hole_birth          active                      local
mypool  feature@extensible_dataset  enabled                     local
mypool  feature@embedded_data       active                      local
mypool  feature@bookmarks           enabled                     local
mypool  feature@filesystem_limits   disabled                    local
mypool  feature@large_blocks        disabled                    local
```

The figure below shows the the total number of operations as a function of
``n`` (i.e. total number of stored key-value pairs). This needs to be done for
a longer number of iterations. However, I don't have the time for this at the
moment, and it seems way more scalable than my needs (the rates seem constant).

![scalability benchmark](https://github.com/mmaakh/fsdb/blob/master/benchmarks/plots/plots.png?raw=true)

You can notice that some of the rates actually increase. This must be due to
ZFS's Adaptive Replacement Cache (ARC).


**Note:** of course, more parameters need testing, such as the effect of key
length, value length, and `dirlen`.


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
     `mystore.delete(KEY, cleanup=BOOLE)`, respectively, where `KEY` must be
     named such that it is a valid file name, `VALUE` can be any arbitrary
     value that is to be stored, and `cleanup` decides whether empty
     directories should be deleted upon the deletion of their key-value pairs.

Example
=======
```python
import fsdb # import the fsdb module
import hashlib # only needed in this specific example to implement the function
               # `myhash`

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

Contact details
===============
``m [ta] khonji [tod] org``.
