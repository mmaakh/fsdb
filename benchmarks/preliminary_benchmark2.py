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
n = 50001
key_prefix = 'testkey'
value_prefix = 'testvalue'

# benchmark the time taken to calculate some md5 hashes (baseline)
sys.stderr.write('benchmarking md5..\n')
f = open('plot_md5', 'w') 
for i in range(1,n):
    start = time.time()
    key = "%s%s" % (key_prefix,i)
    myhash(key)
    end = time.time()
    if i % 1000 == 0:
        f.write("  %s %s\n" % (i, float(1000)/(end-start)))
f.close()

# storing key-value pairs
sys.stderr.write('benchmarking storing key-value pairs..\n')
f = open('plot_store', 'w')
for i in range(1,n):
    start = time.time()
    key = "%s%s" % (key_prefix,i)
    value = "%s%s" % (value_prefix,i)
    mydb.store(key, value)
    end = time.time()
    if i % 1000 == 0:
        f.write("  %s %s\n" % (i, float(1000)/(end-start)))
f.close()

# retrieving key-value pairs
sys.stderr.write('benchmarking retrieving key-value pairs..\n')
f = open('plot_retrieve', 'w')
for i in range(1,n):
    start = time.time()
    key = "%s%s" % (key_prefix,i)
    mydb.retrieve(key)
    end = time.time()
    if i % 1000 == 0:
        f.write("  %s %s\n" % (i, float(1000)/(end-start)))
f.close()

# deleting key-value pairs with deleting empty parent directories
sys.stderr.write('benchmarking deleting key-value pairs with cleanup..\n')
f = open('plot_delete_wcleanup', 'w')
for i in range(1,n):
    start = time.time()
    key = "%s%s" % (key_prefix,i)
    mydb.delete(key)
    end = time.time()
    if i % 1000 == 0:
        f.write("  %s %s\n" % (i, float(1000)/(end-start)))
f.close()

# storing key-value pairs without deleting empty parent directories
sys.stderr.write('preparing for next test..')
for i in range(1,n):
    key = "%s%s" % (key_prefix,i)
    value = "%s%s" % (value_prefix,i)
    mydb.store(key, value)
sys.stderr.write(' ok\n')
sys.stderr.write('benchmarking deleting key-value pairs without cleanup..\n')
f = open('plot_delete_wocleanup', 'w')
for i in range(1,n):
    start = time.time()
    key = "%s%s" % (key_prefix,i)
    mydb.delete(key, cleanup=False)
    end = time.time()
    if i % 1000 == 0:
        f.write("  %s %s\n" % (i, float(1000)/(end-start)))
f.close()

# retrieving none-existent key-value pairs
sys.stderr.write('benchmarking retrieving nonexistent key-value pairs..\n')
f = open('plot_retrieve_notfound', 'w')
for i in range(1,n):
    start = time.time()
    key = "%s%s" % (key_prefix,i)
    mydb.retrieve(key)
    end = time.time()
    if i % 1000 == 0:
        f.write("  %s %s\n" % (i, float(1000)/(end-start)))
f.close()
