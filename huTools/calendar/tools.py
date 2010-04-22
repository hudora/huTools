#!/usr/bin/env python
# encoding: utf-8
"""
tools.py - Functions for date manipulation

Created by Christian Klein on 2010-04-22.
Copyright (c) 2010 HUDORA GmbH. All rights reserved.
"""

import datetime
import unittest


def date_trunc(date, trtype):
    """
    Truncate date
    
    This function is inspired by date_trunc from PostgreSQL, see
    http://www.postgresql.org/docs/8.1/static/functions-datetime.html#FUNCTIONS-DATETIME-TRUNC
    """
    
    tmp = date.timetuple()    
    if trtype == "year":
        return datetime.datetime(tmp.tm_year, 1, 1)
    elif trtype == "month":
        return datetime.datetime(tmp.tm_year, tmp.tm_mon, 1)
    elif trtype == "week":
        firstday = date - datetime.timedelta(days=tmp.tm_wday)
        return datetime.datetime.combine(firstday, datetime.time(0))
    elif trtype == "day":
        return datetime.datetime(tmp.tm_year, tmp.tm_mon, tmp.tm_mday)
    elif trtype == "hour":
        return datetime.datetime(tmp.tm_year, tmp.tm_mon, tmp.tm_mday, tmp.tm_hour)
    elif trtype == "minute":
        return datetime.datetime(tmp.tm_year, tmp.tm_mon, tmp.tm_mday, tmp.tm_hour, tmp.tm_min)
    elif trtype == "second":
        return datetime.datetime(tmp.tm_year, tmp.tm_mon, tmp.tm_mday, tmp.tm_hour, tmp.tm_min, tmp.tm_sec)
    else:
        raise ValueError("Unknown ")

class DateTruncTestCase(unittest.TestCase):
    
    def test_truncate_year(self):
        self.assertEqual(date_trunc(datetime.datetime(1980, 5, 4), 'year'), datetime.datetime(1980, 1, 1))
        self.assertEqual(date_trunc(datetime.datetime(1980, 5, 4), 'year').date(), datetime.date(1980, 1, 1))
        self.assertEqual(date_trunc(datetime.date(1980, 5, 4), 'year'), datetime.datetime(1980, 1, 1, 0, 0, 0))
        self.assertEqual(date_trunc(datetime.date(1980, 5, 4), 'year').date(), datetime.date(1980, 1, 1))
    
    def test_truncate_month(self):
        self.assertEqual(date_trunc(datetime.datetime(1978, 6, 12), 'month'), datetime.datetime(1978, 6, 1))
        self.assertEqual(date_trunc(datetime.datetime(1978, 6, 12), 'month').date(), datetime.date(1978, 6, 1))
        self.assertEqual(date_trunc(datetime.date(1978, 6, 12), 'month'), datetime.datetime(1978, 6, 1, 0, 0, 0))
        self.assertEqual(date_trunc(datetime.date(1978, 6, 12), 'month').date(), datetime.date(1978, 6, 1))
    
    def test_truncate_week(self):
        self.assertEqual(date_trunc(datetime.datetime(2000, 1, 1), 'week'), datetime.datetime(1999, 12, 27))
        self.assertEqual(date_trunc(datetime.datetime(2000, 1, 1), 'week').date(), datetime.date(1999, 12, 27))
        self.assertEqual(date_trunc(datetime.date(2000, 1, 1), 'week'), datetime.datetime(1999, 12, 27, 0, 0, 0))
        self.assertEqual(date_trunc(datetime.date(2000, 1, 1), 'week').date(), datetime.date(1999, 12, 27))
    
    def test_truncate_day(self):
        self.assertEqual(date_trunc(datetime.datetime(2006, 2, 25, 23, 17, 40), 'day'), datetime.datetime(2006, 2, 25))
        self.assertEqual(date_trunc(datetime.datetime(2006, 2, 25), 'day'), datetime.datetime(2006, 2, 25))
        self.assertEqual(date_trunc(datetime.date(2006, 2, 25), 'day'), datetime.datetime(2006, 2, 25, 0, 0, 0))
        self.assertEqual(date_trunc(datetime.date(2006, 2, 25), 'day').date(), datetime.date(2006, 2, 25))
    
    def test_truncate_hour(self):
        self.assertEqual(date_trunc(datetime.datetime(2006, 2, 25, 23, 17, 40), 'hour'), datetime.datetime(2006, 2, 25, 23))
        self.assertEqual(date_trunc(datetime.datetime(2006, 2, 25, 23, 17, 40), 'hour'), datetime.datetime(2006, 2, 25, 23, 0, 0))
        self.assertEqual(date_trunc(datetime.date(2006, 2, 25), 'hour'), datetime.datetime(2006, 2, 25, 0, 0, 0))
        self.assertEqual(date_trunc(datetime.date(2006, 2, 25), 'hour').date(), datetime.date(2006, 2, 25))
    
    def test_truncate_minute(self):
        self.assertEqual(date_trunc(datetime.datetime(2006, 2, 25, 23, 17, 40), 'minute'), datetime.datetime(2006, 2, 25, 23, 17, 0))
        self.assertEqual(date_trunc(datetime.date(2006, 2, 25), 'minute'), datetime.datetime(2006, 2, 25, 0, 0, 0))
        self.assertEqual(date_trunc(datetime.date(2006, 2, 25), 'minute').date(), datetime.date(2006, 2, 25))
    
    def test_truncate_second(self):
        self.assertEqual(date_trunc(datetime.datetime(2006, 2, 25, 23, 17, 40), 'second'), datetime.datetime(2006, 2, 25, 23, 17, 40))
        self.assertEqual(date_trunc(datetime.date(2006, 2, 25), 'second'), datetime.datetime(2006, 2, 25, 0, 0, 0))
        self.assertEqual(date_trunc(datetime.date(2006, 2, 25), 'second').date(), datetime.date(2006, 2, 25))
    
    def test_invalid(self):
        self.assertRaises(ValueError, date_trunc, datetime.datetime.now(), 'alex')
        self.assertRaises(AttributeError, date_trunc, 'alex', 'day')


if __name__ == "__main__":
    unittest.main()