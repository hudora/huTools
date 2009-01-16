# -*- coding: utf-8 -*-

"""Module for robust typecasts."""

from types import ListType, TupleType

def io0(data, default=0):
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
    >>> io0(None, default=0xaffe)
    45054
    """

    try:
        if type(data) in (ListType, TupleType):
            if data and data[0]:
                return int(data[0])
        if data:
            return int(data)
        return default
    except TypeError:
        return default

def float_or_0(data, default=0.0):
    """Helper fnc. Returns data casted to a float value if possible, else to 0.
    
    >>> float_or_0(5.0)
    5.0
    >>> float_or_0(None)
    0.0
    >>> float_or_0(0)
    0.0
    >>> float_or_0(-1)
    -1.0
    >>> float_or_0([])
    0.0
    >>> float_or_0(tuple())
    0.0
    
    """
    if data == None:
        return default
    try:
        return float(data)
    except (TypeError, ValueError):
        # FIXME do we really want to allow to convert anything to zero here or is it better, not to
        # catch the type and value errors an let casting fail?
        return default


if __name__ == '__main__':
    import doctest
    doctest.testmod()
