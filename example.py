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
