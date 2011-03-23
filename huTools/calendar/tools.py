#!/usr/bin/env python
# encoding: utf-8
"""
tools.py - Functions for date manipulation

Created by Christian Klein on 2010-04-22.
Copyright (c) 2010 HUDORA GmbH. All rights reserved.
"""

import datetime
import unittest
import warnings


def date_trunc(trtype, timestamp):
    """
    Truncate date or datetime object. Truncated object of the given type.

    This function is inspired by date_trunc from PostgreSQL, see
    http://www.postgresql.org/docs/8.1/static/functions-datetime.html#FUNCTIONS-DATETIME-TRUNC

    Supported types are year, month, week, day, hour, minute, second.

    >>> date_trunc('week', datetime.datetime(1974, 8, 21))
    datetime.datetime(1974, 8, 19, 0, 0)
    >>> date_trunc('week', datetime.date(1973, 8, 8))
    datetime.date(1973, 8, 6)
    """

    if isinstance(timestamp, basestring):
        # we are called with the old calling convention
        warnings.warn("`date_trunc` should be called with a date/datetime object as the second parameter",
                      DeprecationWarning, stacklevel=2)
        timestamp, trtype = trtype, timestamp

    tmp = timestamp.timetuple()
    if trtype == "year":
        ret = datetime.datetime(tmp.tm_year, 1, 1)
    elif trtype == "month":
        ret = datetime.datetime(tmp.tm_year, tmp.tm_mon, 1)
    elif trtype == "week":
        firstday = timestamp - datetime.timedelta(days=tmp.tm_wday)
        ret = datetime.datetime.combine(firstday, datetime.time(0))
    elif trtype == "day":
        ret = datetime.datetime(tmp.tm_year, tmp.tm_mon, tmp.tm_mday)
    elif trtype == "hour":
        ret = datetime.datetime(tmp.tm_year, tmp.tm_mon, tmp.tm_mday, tmp.tm_hour)
    elif trtype == "minute":
        ret = datetime.datetime(tmp.tm_year, tmp.tm_mon, tmp.tm_mday, tmp.tm_hour, tmp.tm_min)
    elif trtype == "second":
        ret = datetime.datetime(tmp.tm_year, tmp.tm_mon, tmp.tm_mday, tmp.tm_hour, tmp.tm_min, tmp.tm_sec)
    else:
        raise ValueError("Unknown truncation type %s" % trtype)
    # if we where given a datetime object return it, else assume a date object and cast our return
    # value to that
    if isinstance(timestamp, datetime.datetime):
        return ret
    return ret.date()


def get_week(date):
    """
    Calculates the week of the year for a given date
    and returns the year and week number.
    """

    # TODO: the API seems broken. It returns week, year not year, week as documentef
    # why not use date.isocalendar() from the stdlib?

    date = date_trunc('week', date)

    first_monday = date_trunc('week', date_trunc('year', date))
    if first_monday.year < date.year:
        first_monday += datetime.timedelta(weeks=1)
    diff = date_trunc('day', date) - first_monday
    week = 1 + (diff.days / 7)
    return week, first_monday.year


def get_weekspan(date):
    """Gibt den ersten und den letzten Tag der Woche, in der `date` liegt, zurück.

    Dabei ist Montag der erste Tag der woche und Sonntag der letzte.

    >>> get_weekspan(datetime.date(2011, 3, 23))
    (datetime.date(2011, 3, 21), datetime.date(2011, 3, 27))
    """
    startdate = date_trunc('week', date)
    enddate = startdate + datetime.timedelta(days=6)
    return startdate, enddate


class DateTruncTestCase(unittest.TestCase):
    """Unittests for date_trunc"""

    def test_truncate_year(self):
        self.assertEqual(date_trunc('year', datetime.datetime(1980, 5, 4)), datetime.datetime(1980, 1, 1))
        self.assertEqual(date_trunc('year', datetime.datetime(1980, 5, 4)).date(), datetime.date(1980, 1, 1))
        self.assertEqual(date_trunc('year', datetime.date(1980, 5, 4)),
                         datetime.date(1980, 1, 1,))
        self.assertEqual(date_trunc('year', datetime.date(1980, 5, 4)), datetime.date(1980, 1, 1))

    def test_truncate_month(self):
        self.assertEqual(date_trunc('month', datetime.datetime(1978, 6, 12)), datetime.datetime(1978, 6, 1))
        self.assertEqual(date_trunc('month', datetime.datetime(1978, 6, 12)).date(),
                         datetime.date(1978, 6, 1))
        self.assertEqual(date_trunc('month', datetime.date(1978, 6, 12)),
                         datetime.date(1978, 6, 1))
        self.assertEqual(date_trunc('month', datetime.date(1978, 6, 12)), datetime.date(1978, 6, 1))

    def test_truncate_week(self):
        self.assertEqual(date_trunc('week', datetime.datetime(2000, 1, 1)), datetime.datetime(1999, 12, 27))
        self.assertEqual(date_trunc('week', datetime.datetime(2000, 1, 1)).date(),
                         datetime.date(1999, 12, 27))
        self.assertEqual(date_trunc('week', datetime.date(2000, 1, 1)),
                         datetime.date(1999, 12, 27))
        self.assertEqual(date_trunc('week', datetime.date(2000, 1, 1)), datetime.date(1999, 12, 27))

    def test_truncate_day(self):
        self.assertEqual(date_trunc('day', datetime.datetime(2006, 2, 25, 23, 17, 40)),
                         datetime.datetime(2006, 2, 25))
        self.assertEqual(date_trunc('day', datetime.datetime(2006, 2, 25)), datetime.datetime(2006, 2, 25))
        self.assertEqual(date_trunc('day', datetime.date(2006, 2, 25)),
                         datetime.date(2006, 2, 25))
        self.assertEqual(date_trunc('day', datetime.date(2006, 2, 25)), datetime.date(2006, 2, 25))

    def test_truncate_hour(self):
        self.assertEqual(date_trunc('hour', datetime.datetime(2006, 2, 25, 23, 17, 40), ),
                         datetime.datetime(2006, 2, 25, 23))
        self.assertEqual(date_trunc('hour', datetime.datetime(2006, 2, 25, 23, 17, 40)),
                         datetime.datetime(2006, 2, 25, 23, 0, 0))
        self.assertEqual(date_trunc('hour', datetime.date(2006, 2, 25)),
                         datetime.date(2006, 2, 25))
        self.assertEqual(date_trunc('hour', datetime.date(2006, 2, 25)), datetime.date(2006, 2, 25))

    def test_truncate_minute(self):
        self.assertEqual(date_trunc('minute', datetime.datetime(2006, 2, 25, 23, 17, 40)),
                         datetime.datetime(2006, 2, 25, 23, 17, 0))
        self.assertEqual(date_trunc('minute', datetime.date(2006, 2, 25)),
                         datetime.date(2006, 2, 25))
        self.assertEqual(date_trunc('minute', datetime.date(2006, 2, 25)),
                         datetime.date(2006, 2, 25))

    def test_truncate_second(self):
        self.assertEqual(date_trunc('second', datetime.datetime(2006, 2, 25, 23, 17, 40)),
                         datetime.datetime(2006, 2, 25, 23, 17, 40))
        self.assertEqual(date_trunc('second', datetime.date(2006, 2, 25)),
                         datetime.date(2006, 2, 25))
        self.assertEqual(date_trunc('second', datetime.date(2006, 2, 25)),
                         datetime.date(2006, 2, 25))

    def test_invalid(self):
        self.assertRaises(ValueError, date_trunc, 'alex', datetime.datetime.now())


class WeekTestCase(unittest.TestCase):
    """Unittests for get_week"""
    def test_week(self):
        self.assertEqual(get_week(datetime.datetime(1979, 1, 1)), (1, 1979))
        self.assertEqual(get_week(datetime.datetime(1980, 1, 1)), (53, 1979))
        self.assertEqual(get_week(datetime.datetime(1980, 1, 2)), (53, 1979))
        self.assertEqual(get_week(datetime.datetime(1980, 1, 6)), (53, 1979))
        self.assertEqual(get_week(datetime.datetime(1980, 1, 7)), (1, 1980))
        self.assertEqual(get_week(datetime.datetime(1980, 5, 4)), (17, 1980))
        self.assertEqual(get_week(datetime.datetime(1990, 1, 1)), (1, 1990))
        self.assertEqual(get_week(datetime.datetime(1989, 12, 31)), (52, 1989))


class WeekspanTestCase(unittest.TestCase):
    """Unittests for get_weekspan"""

    def test_monday(self):
        """get_weekspan for a monday"""
        date = datetime.date(1981, 5, 4)
        self.assertEqual(date.isoweekday(), 1)
        start_date, end_date = get_weekspan(date)
        self.assertEqual(start_date.isoweekday(), 1)
        self.assertEqual(end_date.isoweekday(), 7)
        self.assertTrue(start_date.toordinal() <= date.toordinal() <= end_date.toordinal())

    def test_tuesday(self):
        """get_weekspan for a tuesday"""
        date = datetime.date(1982, 5, 4)
        self.assertEqual(date.isoweekday(), 2)
        start_date, end_date = get_weekspan(date)
        self.assertEqual(start_date.isoweekday(), 1)
        self.assertEqual(end_date.isoweekday(), 7)
        self.assertTrue(start_date.toordinal() <= date.toordinal() <= end_date.toordinal())

    def test_wednesday(self):
        """get_weekspan for a wednesday"""
        date = datetime.date(1988, 5, 4)
        self.assertEqual(date.isoweekday(), 3)
        start_date, end_date = get_weekspan(date)
        self.assertEqual(start_date.isoweekday(), 1)
        self.assertEqual(end_date.isoweekday(), 7)
        self.assertTrue(start_date.toordinal() <= date.toordinal() <= end_date.toordinal())

    def test_thursday(self):
        """get_weekspan for a thursday"""
        date = datetime.date(1989, 5, 4)
        self.assertEqual(date.isoweekday(), 4)
        start_date, end_date = get_weekspan(date)
        self.assertEqual(start_date.isoweekday(), 1)
        self.assertEqual(end_date.isoweekday(), 7)
        self.assertTrue(start_date.toordinal() <= date.toordinal() <= end_date.toordinal())

    def test_friday(self):
        """get_weekspan for a friday"""
        date = datetime.date(1984, 5, 4)
        self.assertEqual(date.isoweekday(), 5)
        start_date, end_date = get_weekspan(date)
        self.assertEqual(start_date.isoweekday(), 1)
        self.assertEqual(end_date.isoweekday(), 7)
        self.assertTrue(start_date.toordinal() <= date.toordinal() <= end_date.toordinal())

    def test_saturday(self):
        """get_weekspan for a saturday"""
        date = datetime.date(1985, 5, 4)
        self.assertEqual(date.isoweekday(), 6)
        start_date, end_date = get_weekspan(date)
        self.assertEqual(start_date.isoweekday(), 1)
        self.assertEqual(end_date.isoweekday(), 7)
        self.assertTrue(start_date.toordinal() <= date.toordinal() <= end_date.toordinal())

    def test_sunday(self):
        """get_weekspan for a sunday"""
        date = datetime.date(1980, 5, 4)
        self.assertEqual(date.isoweekday(), 7)
        start_date, end_date = get_weekspan(date)
        self.assertEqual(start_date.isoweekday(), 1)
        self.assertEqual(end_date.isoweekday(), 7)
        self.assertTrue(start_date.toordinal() <= date.toordinal() <= end_date.toordinal())


if __name__ == "__main__":
    import doctest
    import sys
    failure_count, test_count = doctest.testmod()
    unittest.main()
    sys.exit(failure_count)
