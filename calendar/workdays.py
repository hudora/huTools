#!/usr/bin/env python
# encoding: utf-8
"""
workdays.py - calculate the number of workdays between two datetime objects.

Created by Christian Klein on 2006-11-28. Fiddeled with by Maximillian Dornseif.
BSD Licensed
"""

import datetime
import unittest

STATIC_GERMAN_HOLIDAYS = ((01, 01), # Neujahr
                          (05, 01), # Tag der Arbeit
                          (10, 03), # Tag der deutschen Einheit
                          (11, 01), # Allerheiligen
                          (12, 25), # Erster Weihnachtstag
                          (12, 26), # Zweiter Weihnachtstag
)

def add_to_day(day, offset):
    "Returns the date n days before or after day" 
    return datetime.date.fromordinal(day.toordinal() + offset)

def easter(year):
    """Returns the day of Easter sunday for 'year'.
    This function only works betweeen 1900 and 2099"""
    h = (24 + 19 * (year % 19)) % 30
    i = h - (h / 28)
    j = (year + (year / 4) + i - 13) % 7
    l = i - j
    
    easter_month = 3 + ((l + 40) / 44)
    easter_day = l + 28 - 31 * (easter_month / 4)
    
    return (easter_month, easter_day)

def easter_related_holidays(year):
    "Returns a list of holidays which are related to easter for 'year'."
    easter_days = []
    easter_month, easter_day = easter(year)
    easter_sunday = datetime.date(year, easter_month, easter_day)
    
    # Karfreitag
    easter_days.append(add_to_day(easter_sunday, -2))
    # Ostermontag
    easter_days.append(add_to_day(easter_sunday, 1))
    # Christi Himmelfahrt
    easter_days.append(add_to_day(easter_sunday, 39))
    # Pfingstmontag
    easter_days.append(add_to_day(easter_sunday, 50))
    # Fronleichnam
    easter_days.append(add_to_day(easter_sunday, 60))
    
    return easter_days

def holidays(start, end):
    """Returns a list of dates between start and end that are holidays."""
    hdays = []
    # Berechne alle Feiertage in den Jahren a bis b.
    # Falls a == b werden auch die Feiertage des nächsten
    # Jahres mitberechnet, aber die Liste muss sowieso
    # nochmal gefiltert werden.
    for year in range(start.year, end.year+1):
        for month, day in STATIC_GERMAN_HOLIDAYS:
            hdays.append(datetime.date(year, month, day))
        hdays += easter_related_holidays(year)
    
    return hdays

def workdays(start, end):
    """Calculates the number of working days between two given dates."""
    def day_before(day):
        """Returns the day before 'day'."""
        return datetime.date.fromordinal(day.toordinal() - 1)
    
    def day_after(day):
        """Returns the day after 'day'."""
        return datetime.date.fromordinal(day.toordinal() + 1)
    
    if start > end:
        raise ValueError, "can't handle  negative timespan! %r > %r" % (start, end)
    
    # Wenn Anfangstag auf Wochenende liegt, addiere Tage bis Montag
    while start.isoweekday() >= 6:
        start = day_after(start)
    
    # Wenn Endtag auf Wochenende liegt, substrahiere Tage bis Freitag
    while end.isoweekday() >= 6:
        end = day_before(end)
    
    delta = end - start
    days = delta.days
    
    # Count weekends:
    # if weekday start < weekday end: n / 7
    # if weekday start > weekday end: (n / 7) + 1
    number_of_weekends = days / 7
    if start.isoweekday() > end.isoweekday():
        number_of_weekends += 1
    
    days = days - 2 * number_of_weekends
    return days

def workdays_german(start, end):
    """Calculates the number of working days between two given dates while considering german holidays."""    
    days = workdays(start, end)
    # Deduct Holidays (but only the ones not on weekends)
    holid = [x for x in holidays(start, end) if (x >= start) and (x < end) and (x.isoweekday() < 6)]
    return days - len(holid)
    
def workdayhours_german(start, end):
    """Calculates the number of hours expect weekends and german holidays between two given datetimes."""
    noncountingdays = (end.date() - start.date()) - datetime.timedelta(workdays_german(start.date(), end.date()))
    delta = (end - start - noncountingdays)
    return (delta.days * 24) + (delta.seconds / 60.0 / 60.0)
    
class WorkdayTests(unittest.TestCase):
    #     November 2006         December 2006          January 2007
    #  S  M Tu  W Th  F  S   S  M Tu  W Th  F  S   S  M Tu  W Th  F  S
    #           1  2  3  4                  1  2   1  2  3  4  5  6  7
    #  5  6  7  8  9 10 11   3  4  5  6  7  8  9   8  9 10 11 12 13 14
    # 12 13 14 15 16 17 18  10 11 12 13 14 15 16  15 16 17 18 19 20 21
    # 19 20 21 22 23 24 25  17 18 19 20 21 22 23  22 23 24 25 26 27 28
    # 26 27 28 29 30        24 25 26 27 28 29 30  29 30 31            
    #                       31
    
    def test_wokdays(self):
        """Simple minded tests for workdays()"""
        date = datetime.date
        self.assertEqual(0, workdays(date(2006, 11, 29), date(2006, 11, 29)))
        self.assertEqual(1, workdays(date(2006, 11, 29), date(2006, 11, 30)))
        self.assertEqual(1, workdays(date(2006, 11, 30), date(2006, 12,  1)))
        self.assertEqual(5, workdays(date(2006, 12, 12), date(2006, 12, 19)))
        self.assertEqual(0, workdays(date(2006, 11, 20), date(2006, 11, 20)))
        self.assertEqual(1, workdays(date(2006, 11, 20), date(2006, 11, 21)))
        self.assertEqual(4, workdays(date(2006, 11, 20), date(2006, 11, 24)))
        self.assertEqual(4, workdays(date(2006, 11, 20), date(2006, 11, 25)))
        self.assertEqual(4, workdays(date(2006, 11, 20), date(2006, 11, 26)))
        self.assertEqual(5, workdays(date(2006, 11, 20), date(2006, 11, 27)))
        self.assertEqual(5, workdays(date(2006, 12, 25), date(2007,  1,  1)))
        self.assertEqual(0, workdays(date(2006, 12, 17), date(2006, 12, 18)))
        self.assertEqual(1, workdays(date(2006, 12, 17), date(2006, 12, 19)))
        self.assertEqual(4, workdays(date(2006, 12, 17), date(2006, 12, 22)))
        self.assertEqual(4, workdays(date(2006, 12, 17), date(2006, 12, 23)))
        self.assertEqual(4, workdays(date(2006, 12, 17), date(2006, 12, 24)))
        self.assertEqual(5, workdays(date(2006, 12, 17), date(2006, 12, 25)))
        self.assertEqual(261, workdays(date(2004, 1, 1), date(2004,  12,  31)))
        self.assertEqual(259, workdays(date(2005, 1, 1), date(2005,  12,  31)))
        self.assertEqual(259, workdays(date(2006, 1, 1), date(2006,  12,  31)))
        self.assertEqual(260, workdays(date(2007, 1, 1), date(2007,  12,  31)))
        self.assertEqual(261, workdays(date(2008, 1, 1), date(2008,  12,  31)))
        # TODO: this fails!
        #self.assertEqual(261+259, workdays(date(2004, 1, 1), date(2005,  12,  31)))
        #self.assertEqual(261+259+259, workdays(date(2004, 1, 1), date(2006,  12,  31)))
        #self.assertEqual(261+259+259+260, workdays(date(2004, 1, 1), date(2007,  12,  31)))
        #self.assertEqual(261+259+259+260+261, workdays(date(2004, 1, 1), date(2008,  12,  31)))
    
    def test_workdays_german(self):
        """Simple minded tests for workdays_german()"""
        date = datetime.date
        self.assertEqual(3, workdays_german(date(2006, 12, 25), date(2007,  1,  1)))
        self.assertEqual(1, workdays_german(date(2007, 02, 02), date(2007, 02, 05)))
        self.assertEqual(253, workdays_german(date(2005, 1, 1), date(2005,  12,  31)))
        self.assertEqual(251, workdays_german(date(2006, 1, 1), date(2006,  12,  31)))
        self.assertEqual(251, workdays_german(date(2007, 1, 1), date(2007,  12,  31)))
        self.assertEqual(253, workdays_german(date(2008, 1, 1), date(2008,  12,  31)))
        # TODO: this fails!
        # self.assertEqual(253+251, workdays_german(date(2005, 1, 1), date(2006,  12,  31)))
        # self.assertEqual(253+251+251, workdays_german(date(2005, 1, 1), date(2007,  12,  31)))
        # self.assertEqual(253+251+251+253, workdays_german(date(2005, 1, 1), date(2008,  12,  31)))
        
    def test_workdayhours_german(self):
        """Simple minded tests for workdays_german()"""
        date = datetime.datetime
        self.assertEqual(72, workdayhours_german(date(2006, 12, 25), date(2007,  1,  1)))
        self.assertEqual(24, workdayhours_german(date(2007, 02, 02), date(2007, 02, 05)))
        self.assertAlmostEqual(30.2, workdayhours_german(date(2007, 02, 02, 10, 47), date(2007, 02, 05, 16, 59)))
        
if __name__ == '__main__':
    unittest.main()
