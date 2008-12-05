# -*- coding: utf-8 -*-

"""Module for robust typecasts."""

from types import ListType, TupleType

def io0(data):
    """Wandelt "None" in 0, lässt alle anderen werte unverändert.
    
    >>> io0(5)
    5
    >>> io0(None)
    0
    >>> io0(0)
    0
    >>> io0(-1)
    -1
    >>> io0([])
    0
    >>> io0(tuple())
    0
    
    """

    try:
        if type(data) in (ListType, TupleType):
            if data and data[0]:
                return int(data[0])
        if data:
            return int(data)
        return 0
    except TypeError:
        return 0

if __name__ == '__main__':
    import doctest
    doctest.testmod()
