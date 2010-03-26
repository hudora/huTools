#!/usr/bin/env python
# encoding: utf-8
"""
bank.py

Created by Christian Klein on 2010-03-25.
Copyright (c) 2010 Christian Klein. All rights reserved.
"""

from string import ascii_uppercase

def convert_character(string):
    """Konvertierung von nicht-numerischen Zeichen in einer IBAN"""
    result = []
    for character in string:
        if character.isdigit():
            result.append(character)
        else:
            result.append(str(ascii_uppercase.index(character) + 10))

    return "".join(result)


def iban(ktonr, blz, land="DE"):
    """
    Berechnet die International Bank Account Number für deutsche Konten
    
    Zunächst wird die Basic Bank Account Number für deutsche Konten berechnet.
    Der Laendercode wird mit zwei '0' aufgefüllt und an die BBAN gehangen.
    Aus diesem wird der Prüfcode als Modulo 97-10 (DIN ISO 7064) berechnet.

    >>> 
    """
    
    bban = "%08d%010d" % (int(blz), int(ktonr))
    tmp = convert_character("%s%s00" % (bban, land))
    pruefziffer = 98 - (int(tmp) % 97)
    return "%s%02d%s" % (land, pruefziffer, bban)


def check_iban(value):
    """Validiere (errechnete) IBAN"""
    return int(convert_character(value[4:] + value[:4])) % 97 == 1
