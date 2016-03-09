import fsdb
import hashlib

def hashf(key):
    return hashlib.md5(key.encode('utf8')).hexdigest()

mydb = fsdb.storage('./storage_root', f=hashf)

key = 'testkey'

mydb.store(key, 'testvalue')
