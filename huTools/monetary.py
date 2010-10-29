#!/usr/bin/env python
# encoding: utf-8
"""
monetary.py -

Created by Christian Klein on 2010-03-25.
Copyright (c) 2010 Christian Klein. All rights reserved.
"""

import decimal


def cent_to_euro(amount):
    """
    Rechnet einen Cent-Betrag nach Euro um, inklusive Rundung

    Es wird mit ROUND_HALF_DOWN gerundet.

    >>> cent_to_euro(100)
    Decimal('1.00')
    >>> cent_to_euro(50)
    Decimal('0.50')
    >>> cent_to_euro(1)
    Decimal('0.01')
    >>> cent_to_euro('0.1')
    Decimal('0.00')
    """

    value = decimal.Decimal(amount) / 100
    return value.quantize(decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_DOWN)


def euro_to_cent(amount):
    """
    Rechnet einen Cent-Betrag nach Euro um, inklusive Rundung

    Es wird mit ROUND_HALF_DOWN gerundet.

    >>> euro_to_cent(1)
    Decimal('100')
    >>> euro_to_cent('0.5')
    Decimal('50')
    >>> euro_to_cent('0.01')
    Decimal('1')
    >>> euro_to_cent('0.001')
    Decimal('0')
    """

    value = decimal.Decimal(amount) * 100
    return value.quantize(decimal.Decimal("1"), rounding=decimal.ROUND_HALF_DOWN)


def netto(amount, tax=19):
    """
    Mehrwertsteuer aus den Preisen rausrechnen.

    >>> netto(decimal.Decimal('1.19'))
    Decimal('1.00')
    """

    amount /= decimal.Decimal("1.%d" % tax)
    return amount.quantize(decimal.Decimal("0.01"), rounding=decimal.ROUND_HALF_DOWN)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
