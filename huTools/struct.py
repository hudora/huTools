# encoding: utf-8

"""

Created 2010-06-04 by MAximillian Dornseif
Copyright (c) 2010 HUDORA. All rights reserved."""


import collections


# siehe http://stackoverflow.com/questions/1305532/convert-python-dict-to-object
class Struct(object):
    def __init__(self, entries, default=None):
        self.__dict__.update(entries)
        self.default = default

    def __getattr__(self, name):
        return self.default


def make_struct(obj):
    """Converts a dict to an object, leaves the object untouched.
    Read Only!
    """
    if not hasattr(obj, '__dict__') and isinstance(obj, collections.Mapping):
        struct = Struct(obj)
        for k, v in obj.items():
            setattr(struct, k, make_struct(v))
        return struct
    return obj


if __name__ == '__main__':
    d = make_struct({
        'item1': 'string',
        'item2': ['dies', 'ist', 'eine', 'liste'],
        'item3': dict(dies=1, ist=2, ein=3, dict=4),
        'item4': 10,
        'item5': [dict(dict=1, in_einer=2, liste=3)]})
    print type(d)
    print d.item1
    print d.item2
    print d.item3
    print d.item3.dies
    print d.item3.ist
    print d.item3.ein
    print d.item3.dict
    print d.item4
    print d.item5
