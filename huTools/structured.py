# encoding: utf-8

"""
structured.py - handle structured data/dicts/objects

Created 2010-06-04 by Maximillian Dornseif
Copyright (c) 2010 HUDORA. All rights reserved."""


# siehe http://stackoverflow.com/questions/1305532/convert-python-dict-to-object
class Struct(object):
    def __init__(self, entries, default=None):
        self.__dict__.update(entries)
        self.default = default

    def __getattr__(self, name):
        if name.startswith('_'):
            # copy expects __deepcopy__, __getnewargs__ to raise AttributeError
            # see http://groups.google.com/group/comp.lang.python/browse_thread/thread/6ac8a11de4e2526f/e76b9fbb1b2ee171?#e76b9fbb1b2ee171
            raise AttributeError("'<Struct>' object has no attribute '%s'" % name)
        return self.default

    #def __setattr__(self, name, value):
    #    raise TypeError('Struct objects are immutable')


def make_struct(obj, default=None):
    """Converts a dict to an object, leaves the object untouched.
    Read Only!
    """
    if not hasattr(obj, '__dict__') and isinstance(obj, collections.Mapping):
        struct = Struct(obj, default=default)
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
