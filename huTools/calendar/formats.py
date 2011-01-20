#!/usr/bin/env python
# encoding: utf-8
"""
formats.py - formating and parsing of timestamps.

Created by Maximillian Dornseif on 2007-06-24.
Copyright (c) 2007, 2010 HUDORA GmbH. All rights reserved.
"""

import unittest
import datetime
import time
import email.utils


def rfc3339_date(date=None):
    """Formates a datetime object according to RfC 3339."""
    date = date or datetime.datetime.now()
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')


def rfc3339_date_parse(date):
    """Parses an RfC 3339 timestamp into a datetime object."""
    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')


def convert_to_date(date):
    """
    Converts argument into a date object.

    Assumes argument to be a RfC 3339 coded date or a date(time) object.
    """

    if hasattr(date, 'date') and callable(date.date):
        # e.g. datetime objects
        return date.date()
    elif isinstance(date, datetime.date):
        return date
    elif isinstance(date, basestring):
        date = date[:10]  # strip timestamp
        try:
            return datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return datetime.datetime.strptime(date, '%Y%m%d').date()
    elif not date:
        return None
    raise ValueError("Unknown value %r (%s)" % (date, type(date)))


def convert_to_datetime(date):
    """Converts argument into a datetime object.

    Assumes argument to be a RfC 3339 coded date or a date(time) object.
    """

    if isinstance(date, datetime.datetime):
        return date
    elif isinstance(date, datetime.date):  # order mattes! datetime is a subclass of date
        return datetime.datetime(date.year, date.month, date.day)
    elif isinstance(date, basestring):
        if len(date) < 11:
            return convert_to_datetime(convert_to_date(date))
        else:
            ms = 0
            if '.' in date:
                date, ms = date.split('.')
            date = date.rstrip('Z')
            try:
                ret = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                try:
                    ret = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    ret = datetime.datetime.strptime(date, '%Y%m%dT%H%M%S')
            if ms:
                return datetime.datetime(ret.year, ret.month, ret.day,
                                         ret.hour, ret.minute, ret.second, int(ms))
            return ret
    elif not date:
        return None
    raise ValueError("Unknown value %r (%s)" % (date, type(date)))


def rfc2616_date(date=None):
    """Formates a datetime object according to RfC 2616.

    RfC 2616 is a subset of RFC 1123 date.
    Weekday and month names for HTTP date/time formatting; always English!
    """
    date = date or datetime.datetime.now()
    return email.utils.formatdate(time.mktime(date.timetuple()), usegmt=True)


def rfc2616_date_parse(data):
    """Parses an RfC 2616/2822 timestapm into a datetime object."""
    return datetime.datetime.fromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz(data)))


class _FormatsTests(unittest.TestCase):

    def test_rfc3339_date(self):
        """Test basic rfc3339_date output."""
        self.assertEqual(rfc3339_date(datetime.datetime(2007, 2, 3, 4, 5, 6)), '2007-02-03T04:05:06Z')

    def test_rfc3339_date_parse(self):
        """Test basic rfc3339_date_parse output."""
        self.assertEqual(rfc3339_date_parse('2007-02-03T04:05:06Z'),
                         datetime.datetime(2007, 2, 3, 4, 5, 6))

    def test_rfc2616_date(self):
        """Test basic rfc2616_date output."""
        self.assertEqual(rfc2616_date(datetime.datetime(2007, 2, 3, 4, 5, 6)),
                         'Sat, 03 Feb 2007 03:05:06 GMT')

    def test_rfc2616_date_parse(self):
        """Test basic rfc2616_date_parse output."""
        self.assertEqual(rfc2616_date_parse('Sat, 03 Feb 2007 03:05:06 GMT'),
                         datetime.datetime(2007, 2, 3, 4, 5, 6))

    def test_convert_to_datetime(self):
        """Test convert_to_datetime() and convert_to_date() functionality"""
        self.assertEqual(convert_to_datetime(datetime.date(2007, 2, 3)),
                                             datetime.datetime(2007, 2, 3, 0, 0))
        self.assertEqual(convert_to_datetime(datetime.datetime(2007, 2, 3, 13, 14, 15, 16)),
                                             datetime.datetime(2007, 2, 3, 13, 14, 15, 16))
        self.assertEqual(convert_to_datetime('2007-02-03'), datetime.datetime(2007, 2, 3, 0, 0))
        self.assertEqual(convert_to_datetime('2007-2-3'), datetime.datetime(2007, 2, 3, 0, 0))
        self.assertEqual(convert_to_datetime('20070203'), datetime.datetime(2007, 2, 3, 0, 0))
        self.assertEqual(convert_to_datetime('20070203T131415'), datetime.datetime(2007, 2, 3, 13, 14, 15))
        self.assertEqual(convert_to_datetime('2007-02-03T13:14:15'),
                         datetime.datetime(2007, 2, 3, 13, 14, 15))
        self.assertEqual(convert_to_datetime('2007-02-03T13:14:15.16'),
                         datetime.datetime(2007, 2, 3, 13, 14, 15, 16))
        self.assertEqual(convert_to_datetime('2007-02-03 13:14:15'),
                         datetime.datetime(2007, 2, 3, 13, 14, 15))
        self.assertEqual(convert_to_datetime('2007-02-03 13:14:15.16'),
                         datetime.datetime(2007, 2, 3, 13, 14, 15, 16))


class _ApiTests(unittest.TestCase):

    def test_defaults(self):
        """Test rfc3339_date defaults"""
        rfc3339_date()
        rfc2616_date()


if __name__ == '__main__':
    unittest.main()
