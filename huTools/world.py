#!/usr/bin/env python
# encoding: utf-8
"""
world.py - countries of the world (to be procise: countries we do buiseness with)

Created by Maximillian Dornseif on 2007-05-01.
Copyright (c) 2007 HUDORA GmbH. BSD Licensed.
"""

import doctest
import sys

__revision__ = "$Revision$"

COUNTRY_CHOICES = [('DE', 'Deutschland')] \
                   + sorted([
                   ('AT', u'Österreich'),
                   ('CH', 'Schweiz'),
                   ('BE', 'Belgien'),
                   ('FR', 'Frankreich'),
                   ('ES', 'Spanien'),
                   ('NL', 'Niederlande'),
                   ('IT', 'Italien'),
                   ('GB', 'Grossbritannien'),
                   ('LI', 'Liechtenstein'),
                   ('LU', 'Luxemburg'),
                   ('PT', 'Portugal'),
                   ('CZ', 'Tschechien'),
                   ('SE', 'Schweden'),
                   ('GR', 'Griechenland'),
                   ('DK', 'Daenemark'),
                   ('US', 'USA'),
                   ('AR', 'Argentinien'),
                   ('HU', 'Ungarn'),
                   ('LV', 'Lettland'),
                   ('PL', 'Polen'),
                   ('LT', 'Litauen'),
                   ('SK', 'Slowakei'),
                   ('HR', 'Kroatien'),
                   ('IE', 'Irland'),
                   ('SI', 'Slowenien'),
                   ('EE', 'Estland'),
                   ('BG', 'Bulgarien'),
                   ('NO', 'Norwegen'),
                   ('AU', 'Australien'),
                   ('IL', 'Israel'),
                   ('FI', 'Finnland'),
                   ('RS', 'Republik Serbien'),
                   ('ZA', u'Südafrika'),
                   ('RO', u'Rumänien'),
                  ])


# Stand: Mai 2009
EUROPEAN_UNION = ['BE', 'IT', 'RO', 'BG', 'LV', 'SE',
                  'DK', 'LT', 'SK', 'DE', 'LU', 'SI',
                  'EE', 'MT', 'ES', 'FI', 'NL', 'CZ',
                  'FR', 'AT', 'HU', 'GR', 'PL', 'GB',
                  'IE', 'PT', 'CY']


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
