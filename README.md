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
    * **Compatibility**: both Python 2.x and 3.x.
