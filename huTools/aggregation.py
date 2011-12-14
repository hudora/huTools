#!/usr/bin/env python
# encoding: utf-8
"""
aggregation.py - implement things similar to "group by" in SQL.

Created by Maximillian Dornseif on 2010-03-07.
Copyright (c) 2010, 2011 HUDORA. All rights reserved.
"""


from huTools.calendar.tools import date_trunc


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


def robustmin(data):
    """Like min() but handles empty Lists."""
    if data:
        return min(data)
    return None


def robustmax(data):
    """Like max() but handles empty Lists."""
    if data:
        return max(data)
    return None


def _group_by_x(values, aggregationfunc, keyfunc):
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
        ret.append((key, aggregationfunc(values)))
    ret.sort()
    return ret


def group_by_week(values, aggregationfunc):
    """input should be [(datetime, stuff), ...]

    >>> indata = [(datetime.date(2012, 1, 31), 1154), (datetime.date(2012, 2, 20), 3466),
    ...           (datetime.date(2012, 2, 22), 3440), (datetime.date(2012, 3, 13), 3402),
    ...           (datetime.date(2012, 1, 29), -2), (datetime.date(2012, 2, 27), 3436)]
    >>> group_by_week(indata, min)
    [(datetime.date(2012, 1, 23), -2), (datetime.date(2012, 1, 30), 1154), (datetime.date(2012, 2, 20), 3440), (datetime.date(2012, 2, 27), 3436), (datetime.date(2012, 3, 12), 3402)]
    """
    return _group_by_x(values, aggregationfunc, lambda x: date_trunc('week', x))


def group_by_month(values, aggregationfunc):
    """input should be [(datetime, stuff), ...]

    >>> indata = [(datetime.date(2012, 1, 30), 1), (datetime.date(2012, 1, 31), 3),
    ...           (datetime.date(2012, 1, 1), -1), (datetime.date(2012, 1, 1), 0)]
    >>> group_by_month(indata, min)
    [(datetime.date(2012, 1, 1), -1)]
    >>> group_by_month(indata, max)
    [(datetime.date(2012, 1, 1), 3)]
    >>> group_by_month(indata, avg)
    [(datetime.date(2012, 1, 1), 0.75)]
    """
    return _group_by_x(values, aggregationfunc, lambda x: date_trunc('month', x))


def group_by_quarter(values, aggregationfunc):
    """input should be [(datetime, stuff), ...]

    >>> indata = [(datetime.date(2012, 1, 30), 1), (datetime.date(2012, 1, 31), 3),
    ...           (datetime.date(2012, 1, 1), -1), (datetime.date(2011, 12, 12), 0)]
    >>> group_by_quarter(indata, min)
    [(datetime.date(2011, 10, 1), 0), (datetime.date(2012, 1, 1), -1)]
    """
    return _group_by_x(values, aggregationfunc, lambda x: date_trunc('quarter', x))


def group_by_tertial(values, aggregationfunc):
    """input should be [(datetime, stuff), ...]

    >>> indata = [(datetime.date(2012, 1, 31), 1), (datetime.date(2012, 4, 30), 3),
    ...           (datetime.date(2012, 1, 1), -1), (datetime.date(2011, 12, 12), 0)]
    >>> group_by_tertial(indata, avg)
    [(datetime.date(2011, 9, 1), 0.0), (datetime.date(2012, 1, 1), 1.0)]
    """
    return _group_by_x(values, aggregationfunc, lambda x: date_trunc('tertial', x))


def group_by_year(values, aggregationfunc):
    """input should be [(datetime, stuff), ...]

    >>> indata = [(datetime.date(2012, 1, 31), 1), (datetime.date(2012, 4, 30), 3),
    ...           (datetime.date(2012, 1, 1), -1), (datetime.date(2011, 12, 12), 0)]
    >>> group_by_year(indata, max)
    [(datetime.date(2011, 1, 1), 0), (datetime.date(2012, 1, 1), 3)]
    """
    return _group_by_x(values, aggregationfunc, lambda x: date_trunc('year', x))


def objectfunc(func, objektliste, feldliste, ignore_empty=False):
    """Für jedes Property in `feldliste` der Objekte in `objektliste` func ueber alle properties ausführen.

    Wenn `ignore_empty` übergeben wird, werden leere werte / lull werte nicht an `func` üebrgeben.
    """

    sumdir = {}
    if hasattr(feldliste, 'split'):
        feldliste = feldliste.split()
    for feldname in feldliste:
        if objektliste:
            if ignore_empty:
                sumdir[feldname] = func([getattr(x, feldname, 0)
                                         for x in objektliste
                                         if getattr(x, feldname, 0)])
            else:
                sumdir[feldname] = func([getattr(x, feldname, 0)
                                         for x in objektliste])
        else:
            sumdir[feldname] = 0.0
    return sumdir


def objectsum(objektliste, feldliste):
    """Für jedes property in `feldliste` der Objekte in `objektliste` die Summe ermitteln."""

    return objectfunc(sum, objektliste, feldliste)


def percentages(sumdir, basis, feldliste):
    """Fügt zu `sumdir` die prozentsaetze der keys in `feldliste` zur basis `basis` zu.

    >>> sumdir = dict(gesammt=10, dieter=5, klaus=3)
    >>> percentages(sumdir, 'gesammt', 'dieter klaus')
    >>> sorted(sumdir.items())
    [('dieter', 5), ('dieterp', 50.0), ('gesammt', 10), ('klaus', 3), ('klausp', 30.0)]
    """
    if hasattr(feldliste, 'split'):
        feldliste = feldliste.split()
    for feldname in feldliste:
        if sumdir.get(basis, 0):
            sumdir["%sp" % feldname] = float(sumdir[feldname]) / sumdir[basis] * 100
        else:
            sumdir["%sp" % feldname] = None


if __name__ == "__main__":
    import doctest
    import datetime
    doctest.testmod()
