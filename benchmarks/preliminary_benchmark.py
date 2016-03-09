# this is only a benchmark tool only to give a preliminary estimation of the
# performance.
import fsdb
import hashlib
import time
import sys

# define your hash function, here we use MD5
def myhash(key):
    return hashlib.md5(key.encode('utf8')).hexdigest()

# instantiate a storage object
mydb = fsdb.storage('./storage_root', f=myhash)

# general benchmark params
n = 10000
key_prefix = 'testkey'
value_prefix = 'testvalue'

# benchmark the time taken to calculate some md5 hashes (baseline)
sys.stderr.write('benchmarking md5..')
myhash_start = time.time()
for i in range(0,n):
    key = "%s%s" % (key_prefix,i)
    myhash(key)
myhash_end = time.time()
sys.stderr.write(' ok\n')
sys.stderr.write("  md5: %s operations per second\n\n" % (float(n)/(myhash_end-myhash_start)))

# storing key-value pairs
sys.stderr.write('benchmarking storing key-value pairs..')
store_start = time.time()
for i in range(0,n):
    key = "%s%s" % (key_prefix,i)
    value = "%s%s" % (value_prefix,i)
    mydb.store(key, value)
store_end = time.time()
sys.stderr.write(' ok\n')
sys.stderr.write("  store: %s operations per second\n\n" % (float(n)/(store_end-store_start)))

# retrieving key-value pairs
sys.stderr.write('benchmarking retrieving key-value pairs..')
retrieve_start = time.time()
for i in range(0,n):
    key = "%s%s" % (key_prefix,i)
    mydb.retrieve(key)
retrieve_end = time.time()
sys.stderr.write(' ok\n')
sys.stderr.write("  retrieve: %s operations per second\n\n" % (float(n)/(retrieve_end-retrieve_start)))

# deleting key-value pairs with deleting empty parent directories
sys.stderr.write('benchmarking deleting key-value pairs with cleanup..')
delete_start = time.time()
for i in range(0,n):
    key = "%s%s" % (key_prefix,i)
    mydb.delete(key)
delete_end = time.time()
sys.stderr.write(' ok\n')
sys.stderr.write("  delete: %s operations per second\n\n" % (float(n)/(delete_end-delete_start)))

# storing key-value pairs without deleting empty parent directories
sys.stderr.write('preparing for next test..')
for i in range(0,n):
    key = "%s%s" % (key_prefix,i)
    value = "%s%s" % (value_prefix,i)
    mydb.store(key, value)
sys.stderr.write(' ok\n')
sys.stderr.write('benchmarking deleting key-value pairs without cleanup..')
delete_start = time.time()
for i in range(0,n):
    key = "%s%s" % (key_prefix,i)
    mydb.delete(key, cleanup=False)
delete_end = time.time()
sys.stderr.write(' ok\n')
sys.stderr.write("  delete: %s operations per second\n\n" % (float(n)/(delete_end-delete_start)))

# retrieving none-existent key-value pairs
sys.stderr.write('benchmarking retrieving nonexistent key-value pairs..')
delretrieve_start = time.time()
for i in range(0,n):
    key = "%s%s" % (key_prefix,i)
    mydb.retrieve(key)
delretrieve_end = time.time()
sys.stderr.write(' ok\n')
sys.stderr.write("  delretrieve: %s operations per second\n\n" % (float(n)/(delretrieve_end-delretrieve_start)))
