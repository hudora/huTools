#!/usr/bin/env python
# encoding: utf-8
"""
workdays.py - calculate the number of workdays between two datetime objects.

Created by Christian Klein on 2006-11-28. Fiddeled with by Maximillian Dornseif.
BSD Licensed.
"""

import datetime
import doctest
import unittest
import sys
from huTools.decorators import memoize


STATIC_GERMAN_HOLIDAYS = ((1, 1),    # Neujahr
                          (5, 1),    # Tag der Arbeit
                          (10, 3),   # Tag der deutschen Einheit
                          (11, 1),   # Allerheiligen
                          (12, 25),  # Erster Weihnachtstag
                          (12, 26),  # Zweiter Weihnachtstag
)


def add_to_day(day, offset):
    "Returns the date n days before or after day"
    return day + datetime.timedelta(days=offset)


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


@memoize
def holidays_german(start, end):
    """Returns a list of dates between start and end that are holidays."""
    hdays = []
    # Berechne alle Feiertage in den Jahren a bis b.
    # Falls a == b werden auch die Feiertage des nächsten
    # Jahres mitberechnet, aber die Liste muss sowieso
    # nochmal gefiltert werden.
    for year in range(start.year, end.year + 1):
        for month, day in STATIC_GERMAN_HOLIDAYS:
            hdays.append(datetime.date(year, month, day))
        hdays += easter_related_holidays(year)
    return hdays


def workdays(start, end):
    """Calculates the number of working days (Mo-Fr) between two given dates.

    Whereas the workdays are calculated siilar to Python slice notation: [start : end[
    Example:
    >>> workdays(datetime.date(2007, 1, 26), datetime.date(2007,  1,  27)) # Fr - Sa
    1
    >>> workdays(datetime.date(2007, 1, 28), datetime.date(2007,  1,  29)) # Su - Mo
    0
    """

    if start > end:
        raise ValueError("can't handle  negative timespan! %r > %r" % (start, end))

    # Wenn Anfangstag auf Wochenende liegt, addiere Tage bis Montag
    while start.isoweekday() > 5:
        start = add_to_day(start, 1)

    # Wenn Endtag auf Wochenende liegt, substrahiere Tage bis Freitag
    while end.isoweekday() > 5:
        end = add_to_day(end, 1)

    days = (end - start).days

    # Count weekends:
    # if weekday start < weekday end: n / 7
    # if weekday start > weekday end: (n / 7) + 1
    number_of_weekends = days / 7
    if start.isoweekday() > end.isoweekday():
        number_of_weekends += 1
    days = days - 2 * number_of_weekends
    if days < 0:
        raise RuntimeError("%r days difference %r|%r|%r" % (days, start, end, number_of_weekends))
    return days


@memoize
def workdays_german(start, end):
    """Calculates the number of working days between two given dates while considering german holidays."""

    if isinstance(start, datetime.datetime):
        start = start.date()
    if isinstance(end, datetime.datetime):
        end = end.date()

    days = workdays(start, end)
    # Deduct Holidays (but only the ones not on weekends)
    holid = [x for x in holidays_german(start, end) if (x >= start) and (x < end) and (x.isoweekday() < 6)]
    return days - len(holid)


def workdayhours_german(start, end):
    """Calculates the number of hours expect weekends and german holidays between two given datetimes."""
    noncountingdays = (end.date() - start.date()) - \
                       datetime.timedelta(workdays_german(start.date(), end.date()))
    delta = (end - start - noncountingdays)
    return (delta.days * 24) + (delta.seconds / 60.0 / 60.0)


def is_workday_german(day):
    """Checks if a day is a workday in germany (NRW).

    >>> is_workday_german(datetime.date(2007, 1, 1))
    False
    >>> is_workday_german(datetime.date(2007, 1, 2))
    True
    """
    if day.isoweekday() > 5:
        return False  # weekend
    if isinstance(day, datetime.datetime):
        day = day.date()
    return day not in holidays_german(day, day)


@memoize
def next_workday_german(startday):
    """Returns the next workday after startday.

    >>> next_workday_german(datetime.date(2006, 12, 29))
    datetime.date(2007, 1, 2)
    """

    next_day = add_to_day(startday, 1)
    while not is_workday_german(next_day):
        next_day = add_to_day(next_day, 1)
    return next_day


@memoize
def previous_workday_german(startday):
    """Returns the workday before startday.

    >>> previous_workday_german(datetime.date(2007, 1, 2))
    datetime.date(2006, 12, 29)
    """

    prev_day = add_to_day(startday, -1)
    while not is_workday_german(prev_day):
        prev_day = add_to_day(prev_day, -1)
    return prev_day


def add_workdays_german(startday, count):
    """Adds <count> workdays to <startday>."""

    day = startday
    while count > 0:
        day = next_workday_german(day)
        count -= 1
    while count < 0:
        day = previous_workday_german(day)
        count += 1
    return day


class _WorkdayTests(unittest.TestCase):
    """Testcases for workdays module. Calendar hint:
        November 2006         December 2006          January 2007
     S  M Tu  W Th  F  S   S  M Tu  W Th  F  S   S  M Tu  W Th  F  S
              1  2  3  4                  1  2      1  2  3  4  5  6
     5  6  7  8  9 10 11   3  4  5  6  7  8  9   7  8  9 10 11 12 13
    12 13 14 15 16 17 18  10 11 12 13 14 15 16  14 15 16 17 18 19 20
    19 20 21 22 23 24 25  17 18 19 20 21 22 23  21 22 23 24 25 26 27
    26 27 28 29 30        24 25 26 27 28 29 30  28 29 30 31
                          31
    """

    def test_workdays(self):
        """Simple minded tests for workdays()."""
        date = datetime.date

        self.assertEqual(0, workdays(date(2007, 1, 25), date(2007, 1, 25)))    # Th - Th
        self.assertEqual(1, workdays(date(2007, 1, 25), date(2007, 1, 26)))    # Th - Fr
        self.assertEqual(2, workdays(date(2007, 1, 25), date(2007, 1, 27)))    # Th - Sa
        self.assertEqual(1, workdays(date(2007, 1, 26), date(2007, 1, 27)))    # Fr - Sa
        self.assertEqual(1, workdays(date(2007, 1, 26), date(2007, 1, 28)))    # Fr - Su
        self.assertEqual(1, workdays(date(2007, 1, 26), date(2007, 1, 29)))    # Fr - Mo
        self.assertEqual(0, workdays(date(2007, 1, 28), date(2007, 1, 29)))    # Su - Mo
        self.assertEqual(2, workdays(date(2007, 1, 26), date(2007, 1, 30)))    # Fr - Tu
        self.assertEqual(1, workdays(date(2007, 1, 28), date(2007, 1, 30)))    # Su - Tu

        self.assertEqual(0, workdays(date(2007, 1, 26), date(2007, 1, 26)))    # Fr - Fr
        self.assertEqual(1, workdays(date(2007, 1, 26), date(2007, 1, 27)))    # Fr - Sa
        self.assertEqual(1, workdays(date(2007, 1, 26), date(2007, 1, 28)))    # Fr - Su
        self.assertEqual(0, workdays(date(2007, 1, 27), date(2007, 1, 28)))    # Sa - So
        self.assertEqual(0, workdays(date(2007, 1, 27), date(2007, 1, 29)))    # Sa - Mo
        self.assertEqual(1, workdays(date(2007, 1, 27), date(2007, 1, 30)))    # Fr - Tu

        self.assertEqual(0, workdays(date(2006, 11, 29), date(2006, 11, 29)))  # We - We
        self.assertEqual(1, workdays(date(2006, 11, 29), date(2006, 11, 30)))  # We - Th
        self.assertEqual(1, workdays(date(2006, 11, 30), date(2006, 12, 1)))   # Th - Fr
        self.assertEqual(5, workdays(date(2006, 12, 12), date(2006, 12, 19)))  # Tu - Tu
        self.assertEqual(0, workdays(date(2006, 11, 20), date(2006, 11, 20)))
        self.assertEqual(1, workdays(date(2006, 11, 20), date(2006, 11, 21)))
        self.assertEqual(4, workdays(date(2006, 11, 20), date(2006, 11, 24)))
        self.assertEqual(5, workdays(date(2006, 11, 20), date(2006, 11, 25)))  # Mo - Sa
        self.assertEqual(5, workdays(date(2006, 11, 20), date(2006, 11, 26)))  # Mo - Su
        self.assertEqual(5, workdays(date(2006, 11, 20), date(2006, 11, 27)))
        self.assertEqual(5, workdays(date(2006, 12, 25), date(2007, 1, 1)))
        self.assertEqual(6, workdays(date(2006, 12, 8), date(2006, 12, 18)))
        self.assertEqual(5, workdays(date(2006, 12, 9), date(2006, 12, 18)))
        self.assertEqual(0, workdays(date(2006, 12, 17), date(2006, 12, 18)))
        self.assertEqual(1, workdays(date(2006, 12, 17), date(2006, 12, 19)))
        self.assertEqual(4, workdays(date(2006, 12, 17), date(2006, 12, 22)))
        self.assertEqual(5, workdays(date(2006, 12, 17), date(2006, 12, 23)))  # Su - Sa
        self.assertEqual(5, workdays(date(2006, 12, 17), date(2006, 12, 24)))  # Su - Su
        self.assertEqual(5, workdays(date(2006, 12, 17), date(2006, 12, 25)))
        self.assertEqual(261, workdays(date(2004, 1, 1), date(2004, 12, 31)))
        self.assertEqual(260, workdays(date(2005, 1, 1), date(2005, 12, 31)))
        self.assertEqual(260, workdays(date(2006, 1, 1), date(2006, 12, 31)))
        self.assertEqual(260, workdays(date(2007, 1, 1), date(2007, 12, 31)))
        self.assertEqual(261, workdays(date(2008, 1, 1), date(2008, 12, 31)))
        self.assertEqual(260 + 260, workdays(date(2005, 1, 1), date(2006, 12, 31)))
        self.assertEqual(260 + 260 + 260, workdays(date(2005, 1, 1), date(2007, 12, 31)))
        self.assertEqual(260 + 260 + 260, workdays(datetime.datetime(2005, 1, 1),
                                                   datetime.datetime(2007, 12, 31)))

    def test_workdays_german(self):
        """Simple minded tests for workdays_german()."""
        date = datetime.date
        self.assertEqual(0, workdays_german(date(2007, 1, 25), date(2007, 1, 25)))  # Th - Th
        self.assertEqual(1, workdays_german(date(2007, 1, 25), date(2007, 1, 26)))  # Th - Fr
        self.assertEqual(2, workdays_german(date(2007, 1, 25), date(2007, 1, 27)))  # Th - Sa
        self.assertEqual(1, workdays_german(date(2007, 1, 26), date(2007, 1, 27)))  # Fr - Sa
        self.assertEqual(1, workdays_german(date(2007, 1, 26), date(2007, 1, 28)))  # Fr - Su
        self.assertEqual(1, workdays_german(date(2007, 1, 26), date(2007, 1, 29)))  # Fr - Mo
        self.assertEqual(0, workdays_german(date(2007, 1, 28), date(2007, 1, 29)))  # Su - Mo
        self.assertEqual(2, workdays_german(date(2007, 1, 26), date(2007, 1, 30)))  # Fr - Tu
        self.assertEqual(1, workdays_german(date(2007, 1, 28), date(2007, 1, 30)))  # Su - Tu

        self.assertEqual(0, workdays_german(date(2007, 1, 26), date(2007, 1, 26)))  # Fr - Fr
        self.assertEqual(1, workdays_german(date(2007, 1, 26), date(2007, 1, 27)))  # Fr - Sa
        self.assertEqual(1, workdays_german(date(2007, 1, 26), date(2007, 1, 28)))  # Fr - Su
        self.assertEqual(0, workdays_german(date(2007, 1, 27), date(2007, 1, 28)))  # Sa - So
        self.assertEqual(0, workdays_german(date(2007, 1, 27), date(2007, 1, 29)))  # Sa - Mo
        self.assertEqual(1, workdays_german(date(2007, 1, 27), date(2007, 1, 30)))  # Fr - Tu

        self.assertEqual(3, workdays_german(date(2006, 12, 25), date(2007, 1, 1)))
        self.assertEqual(1, workdays_german(date(2007, 2, 2), date(2007, 2, 5)))
        self.assertEqual(252, workdays_german(date(2005, 1, 1), date(2005, 12, 31)))
        self.assertEqual(250, workdays_german(date(2006, 1, 1), date(2006, 12, 31)))
        self.assertEqual(249, workdays_german(date(2007, 1, 1), date(2007, 12, 31)))
        self.assertEqual(251, workdays_german(date(2008, 1, 1), date(2008, 12, 31)))
        # Christi Himmelfahrt
        self.assertEqual(1, workdays_german(date(2007, 5, 16), date(2007, 5, 17)))
        self.assertEqual(1, workdays_german(date(2007, 5, 16), date(2007, 5, 18)))
        self.assertEqual(1, workdays_german(datetime.datetime(2007, 5, 16), datetime.datetime(2007, 5, 18)))
        # Pfingsten
        self.assertEqual(1, workdays_german(date(2007, 5, 24), date(2007, 5, 25)))  # Th - Fr
        self.assertEqual(1, workdays_german(date(2007, 5, 25), date(2007, 5, 26)))  # Fr - Sa
        self.assertEqual(1, workdays_german(date(2007, 5, 25), date(2007, 5, 27)))  # Fr - So
        self.assertEqual(1, workdays_german(date(2007, 5, 25), date(2007, 5, 28)))  # Fr - Mo
        self.assertEqual(1, workdays_german(date(2007, 5, 25), date(2007, 5, 29)))  # Fr - Tu
        # Christi Himmelfahrt
        self.assertEqual(1, workdays_german(date(2007, 6, 6), date(2007, 6, 7)))
        self.assertEqual(1, workdays_german(date(2007, 6, 6), date(2007, 6, 8)))
        self.assertEqual(252 + 250, workdays_german(date(2005, 1, 1), date(2006, 12, 31)))
        self.assertEqual(252 + 250 + 249, workdays_german(date(2005, 1, 1), date(2007, 12, 31)))

        self.assertEqual(252 + 250 + 249, workdays_german(datetime.datetime(2005, 1, 1),
                                                          datetime.datetime(2007, 12, 31)))

    def test_workdayhours_german(self):
        """Simple minded tests for workdays_german()."""
        date = datetime.datetime
        self.assertEqual(72, workdayhours_german(date(2006, 12, 25), date(2007, 1, 1)))
        self.assertEqual(24, workdayhours_german(date(2007, 2, 2), date(2007, 2, 5)))
        self.assertAlmostEqual(30.2, workdayhours_german(date(2007, 2, 2, 10, 47),
                                                         date(2007, 2, 5, 16, 59)))
        self.assertAlmostEqual(30.2, workdayhours_german(datetime.datetime(2007, 2, 2, 10, 47),
                                                         datetime.datetime(2007, 2, 5, 16, 59)))

    def test_is_workday_german(self):
        self.assertTrue(is_workday_german(datetime.date(2011, 4, 21)))  # Gründonnerstag
        self.assertFalse(is_workday_german(datetime.date(2011, 4, 22)))   # karfreitag

        self.assertTrue(is_workday_german(datetime.datetime(2011, 4, 21, 0, 0)))
        self.assertFalse(is_workday_german(datetime.datetime(2011, 4, 22, 0, 0)))

    def test_next_workday_german(self):
        """Simple minded tests for next_workday_german()."""
        date = datetime.date
        self.assertEqual(date(2007, 5, 21), next_workday_german(date(2007, 5, 18)))  # Fr
        self.assertEqual(date(2007, 5, 22), next_workday_german(date(2007, 5, 21)))  # Mo
        self.assertEqual(date(2007, 5, 25), next_workday_german(date(2007, 5, 24)))  # Th
        # Pfingsten
        self.assertEqual(date(2007, 5, 29), next_workday_german(date(2007, 5, 25)))  # Fr
        self.assertEqual(date(2007, 5, 29), next_workday_german(date(2007, 5, 26)))  # Sa
        self.assertEqual(date(2007, 5, 29), next_workday_german(date(2007, 5, 27)))  # Su
        self.assertEqual(date(2007, 5, 29), next_workday_german(date(2007, 5, 28)))  # Mo ( Holiday)
        self.assertEqual(date(2007, 5, 31), next_workday_german(date(2007, 5, 30)))
        self.assertEqual(datetime.datetime(2007, 5, 31), next_workday_german(datetime.datetime(2007, 5, 30)))

    def test_add_workdays_german(self):
        """Simple minded tests for add_workdays_german,"""
        date = datetime.date
        self.assertEqual(date(2008, 11, 24), add_workdays_german(date(2008, 11, 24), 0))
        self.assertEqual(date(2008, 11, 25), add_workdays_german(date(2008, 11, 24), 1))
        self.assertEqual(date(2008, 12, 1), add_workdays_german(date(2008, 11, 24), 5))
        self.assertEqual(date(2008, 11, 21), add_workdays_german(date(2008, 11, 24), -1))
        self.assertEqual(date(2008, 11, 14), add_workdays_german(date(2008, 11, 24), -6))
        self.assertEqual(datetime.datetime(2008, 11, 14),
                         add_workdays_german(datetime.datetime(2008, 11, 24), -6))


if __name__ == '__main__':
    failure_count, test_count = doctest.testmod()
    unittest.main()
    sys.exit(failure_count)
