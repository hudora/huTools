#!/usr/bin/env python
# encoding: utf-8
"""
bank.py

Created by Christian Klein on 2010-03-25.
Copyright (c) 2010 Christian Klein. All rights reserved.
"""


def convert_character(string):
    """Konvertierung von nicht-numerischen Zeichen in IBAN"""
    result = []
    for character in string:
        if character.isdigit():
            result.append(character)
        else:
            result.append(str("ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(character) + 10))

    return "".join(result)


def iban(ktonr, blz, land="DE"):
    """
    Berechnet die International Bank Account Number für deutsche Konten
    
    Zunächst wird die Basic Bank Account Number für deutsche Konten berechnet.
    Aus diesem, XXX
    """
    
    bban = "%08d%010d" % (int(blz), int(ktonr))
    tmp = convert_character("%s%s00" % (bban, land))
    pruefziffer = 98 - (int(tmp) % 97)
    return "%s%02d%s" % (land, pruefziffer, bban)


def check_iban(value):
    return int(convert_character(value[4:] + value[:4])) % 97 == 1


if __name__ == "__main__":
    x = iban("1234567890", "70090100")
    print x
    print check_iban(x)