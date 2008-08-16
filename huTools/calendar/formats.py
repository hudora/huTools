#!/usr/bin/env python
# encoding: utf-8
"""
formats.py - formating and parsing of timestamps.

Created by Maximillian Dornseif on 2007-06-24.
Copyright (c) 2007 HUDORA GmbH. All rights reserved.
"""

import unittest
import datetime, time, email.utils

__revision__ = "$Revision$"

def rfc3339_date(date):
    """Formates a datetime object according to RfC 3339."""
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    
def rfc3339_date_parse(date):
    """Parses an RfC 3339 timestamp into a datetime object."""
    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    
    
# RfC 2616 is a subset of RFC 1123 date
# Weekday and month names for HTTP date/time formatting; always English!
def rfc2616_date(date):
    """Formates a datetime object according to RfC 2616."""
    return email.utils.formatdate(time.mktime(date.timetuple()), usegmt=True)
    
    
def rfc2616_date_parse(data):
    """Parses an RfC 2616/2822 timestapm into a datetime object."""
    return datetime.datetime.fromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz(data)))
    

class _FormatsTests(unittest.TestCase):
    # TODO: investigate handling of timezones.
    
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
    
    
if __name__ == '__main__':
    unittest.main()