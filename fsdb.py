# fsdb - a minimalist but highly scalable key-value store.
#
# Copyright (C) 2016 Mahmoud Khonji <m@khonji.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import os


# CONSTANTS
CODE_PASS = 0
CODE_FAIL = 1


# TRANSFORM A KEY INTO A PATH
def _getpath(root, key, dirlen):
    path = '/'.join(
        [key[i:i+dirlen] for i in range(0, len(key), dirlen)]
    )
    return '%s/%s/' % (root, path)


# FSDB STORAGE CLASS
class storage:
    # set needed configs
    def __init__(self, root, f, dirlen=2, v=True):
        self.root = root
        self.f = f
        self.dirlen = dirlen
        self.v = v

    # store given key-value pair
    def store(self, key, value):
        # define key-value storage path
        path = _getpath(self.root, self.f(key), self.dirlen)

        # create directories if needed
        try:
            os.makedirs(os.path.dirname(path))
        except:
            pass

        # store key-value
        try:
            with open(path + key, 'w') as f:
                f.write(value)
        except Exception as e:
            sys.stderr.write("ERROR: '%s'.\n" % (e))
            sys.exit(CODE_FAIL)

    # retrieve stored value for given key
    def retrieve(self, key):
        # define key-value storage path
        path = _getpath(self.root, self.f(key), self.dirlen)

        # try to retrieve value if exits
        try:
            with open(path + key, 'r') as f:
                value = f.read()
        except:
            value = None

        return value

    # delete key-value pair
    def delete(self, key, cleanup=True):
        # define key-value storage path
        path = _getpath(self.root, self.f(key), self.dirlen)

        # delete the key-value pair and its parent directories if they are
        # empty
        try:
            os.remove(path + key)
            keys = os.listdir(path)
            if (len(keys) == 0) and cleanup:
                try:
                    os.removedirs(path)
                except Exception as e:
                    sys.stderr.write("ERROR: '%s'.\n" % (e))
                    sys.exit(CODE_FAIL)
        except:
            pass
