# -*- coding: utf-8 -*-

"""Module for robust typecasts."""

from types import ListType, TupleType
import doctest
import re
import sys
import warnings


def only_digits(data):
    """Removes all non-digits from a string

    >>> only_digits('0123456789')
    '0123456789'
    >>> only_digits('ab123')
    '123'
    >>> only_digits('1abc')
    '1'
    >>> only_digits('abc')
    ''
    """

    return re.sub(r'[^0-9]', '', data)


def int_or_0(data, default=0):
    """Wandelt "None" in default, lässt alle anderen werte unverändert.

    >>> int_or_0(5)
    5
    >>> int_or_0(None)
    0
    >>> int_or_0(0)
    0
    >>> int_or_0(-1)
    -1
    >>> int_or_0([])
    0
    >>> int_or_0(tuple())
    0
    >>> int_or_0(None, default=0xaffe)
    45054
    """

    if not data:
        return default

    try:
        if isinstance(data, (ListType, TupleType)):
            return int(data[0])
        return int(float(data))
    except (TypeError, ValueError):
        return default


def io0(data):
    warnings.warn("io0() is deprecated. Use int_or_0()", DeprecationWarning, stacklevel=2)
    return int_or_0(data)


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
    if not data:
        return default
    try:
        return float(data)
    except (TypeError, ValueError):
        # FIXME do we really want to allow to convert anything to zero here or is it better, not to
        # catch the type and value errors an let casting fail?
        return default


if __name__ == '__main__':
    failure_count, test_count = doctest.testmod()
    sys.exit(failure_count)
