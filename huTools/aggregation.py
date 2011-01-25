#!/usr/bin/env python
# encoding: utf-8
"""
aggregation.py - implement things similar to "group by" in SQL.

Created by Maximillian Dornseif on 2010-03-07.
Copyright (c) 2010 HUDORA. All rights reserved.
"""


import datetime


def avg(data):
    """Calculate the average of a list.

    >>> avg([1,2,3])
    2.0
    >>> avg([1,1,10])
    4.0
    >>> avg([3])
    3.0
    """

    if data:
        return (sum(data)) / float(len(data))
    return 0.0


def median(data):
    """Calculated the Median of a list.

    >>> median([1,2,3])
    2.0
    >>> median([1,2,3,4])
    2.5
    >>> median([1,2,10])
    2.0
    >>> median([3])
    3.0
    """

    if data:
        sdata = sorted(data)
        if len(sdata) % 2 == 1:
            return float(sdata[(len(sdata) + 1) / 2 - 1])
        else:
            lower = sdata[len(sdata) / 2 - 1]
            upper = sdata[len(sdata) / 2]
            return float(lower + upper) / 2
    return 0.0


def _group_by_x(values, aggregationfunc, keyfunc, reversefunc):
    """input should be [(datetime, stuff), ...]"""

    groupings = {}
    for date, value in values:
        key = keyfunc(date)
        if key not in groupings:
            groupings[key] = [value]
        else:
            groupings[key].append(value)
    ret = []
    for key, values in groupings.items():
        ret.append((reversefunc(key), aggregationfunc(values)))
    ret.sort()
    return ret


def _month_key(date):
    return (date.year, date.month)


def _month_to_date(tup):
    """Reverse of _month_key()"""
    (year, month) = tup
    return datetime.date(year, month, 1)


def _quarter_key(date):
    return (date.year, int(((date.month + 1) / 3) + 1))


def _quarter_to_date(tup):
    """Reverse of _quarter_key()"""
    (year, month) = tup
    return datetime.date(year, month, 1)


def _year_key(date):
    return date.year


def _year_to_date(tup):
    """Reverse of _year_key()"""
    return datetime.date(tup, 1, 1)


def group_by_month(values, aggregationfunc):
    """input should be [(datetime, stuff), ...]"""
    return _group_by_x(values, aggregationfunc, _month_key, _month_to_date)


def group_by_quarter(values, aggregationfunc):
    """input should be [(datetime, stuff), ...]"""
    return _group_by_x(values, aggregationfunc, _quarter_key, _quarter_to_date)


def group_by_year(values, aggregationfunc):
    """input should be [(datetime, stuff), ...]"""
    return _group_by_x(values, aggregationfunc, _year_key, _year_to_date)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
