#!/usr/bin/env python
# encoding: utf-8
"""
hutools/world - countries of the world (to be procise: countries we do buiseness with)

Most interesting are the constants COUNTRY_CHOICES and COUNTRIES.

COUNTRY_CHOICES = [('DE', 'Deutschland'), ('AT', u'Österreich'), ...]
COUNTRIES = ['DE', 'AT', ...]

Created by Maximillian Dornseif on 2007-05-01.
Copyright (c) 2007, 2010 HUDORA GmbH. BSD Licensed.
"""

import doctest
import sys

COUNTRY_CHOICES = [('DE', u'Deutschland'),
                   ('AR', u'Argentinien'),
                   ('AT', u'Österreich'),
                   ('AU', u'Australien'),
                   ('BE', u'Belgien'),
                   ('BG', u'Bulgarien'),
                   ('CH', u'Schweiz'),
                   ('CY', u'Zypern'),
                   ('CZ', u'Tschechien'),
                   ('DK', u'Daenemark'),
                   ('EE', u'Estland'),
                   ('ES', u'Spanien'),
                   ('FI', u'Finnland'),
                   ('FR', u'Frankreich'),
                   ('GB', u'Grossbritannien'),
                   ('GR', u'Griechenland'),
                   ('HR', u'Kroatien'),
                   ('HU', u'Ungarn'),
                   ('IE', u'Irland'),
                   ('IL', u'Israel'),
                   ('IT', u'Italien'),
                   ('LI', u'Liechtenstein'),
                   ('LT', u'Litauen'),
                   ('LU', u'Luxemburg'),
                   ('LV', u'Lettland'),
                   ('MT', u'Malta'),
                   ('NL', u'Niederlande'),
                   ('NO', u'Norwegen'),
                   ('PL', u'Polen'),
                   ('PT', u'Portugal'),
                   ('RO', u'Rumänien'),
                   ('RS', u'Republik Serbien'),
                   ('SE', u'Schweden'),
                   ('SI', u'Slowenien'),
                   ('SK', u'Slowakei'),
                   ('US', u'USA'),
                   ('ZA', u'Südafrika'),
                   ]


COUNTRIES = dict(COUNTRY_CHOICES).keys()


# Stand: Juli 2013 - diese MÜSSEN auch in COUNTRY_CHOICES vorkommen.
EUROPEAN_UNION = ['BE', 'IT', 'RO', 'BG', 'LV', 'SE',
                  'DK', 'LT', 'SK', 'DE', 'LU', 'SI',
                  'EE', 'MT', 'ES', 'FI', 'NL', 'CZ',
                  'FR', 'AT', 'HU', 'GR', 'PL', 'GB',
                  'IE', 'PT', 'CY', 'HR']


def in_european_union(isoland):
    """
    Gibt zurück, ob ein Land Mitglied der EU ist.

    >>> in_european_union('DE')
    True
    >>> in_european_union('CH')
    False
    >>> all(map(in_european_union, EUROPEAN_UNION))
    True
    >>> non_eu_countries = set((abrev for abrev, name in COUNTRY_CHOICES)) - set(EUROPEAN_UNION)
    >>> any(map(in_european_union, non_eu_countries))
    False
    """

    return isoland.upper() in EUROPEAN_UNION

if __name__ == "__main__":
    failure_count, test_count = doctest.testmod()
    sys.exit(failure_count)
