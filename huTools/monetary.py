#!/usr/bin/env python
# encoding: utf-8
"""
monetary.py

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
    return value.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_DOWN)


def euro_to_cent(amount, coerce=int):
    """
    Rechnet einen Cent-Betrag nach Euro um, inklusive Rundung

    Es wird mit ROUND_HALF_DOWN gerundet.

    >>> euro_to_cent(1)
    100
    >>> euro_to_cent('0.5')
    50
    >>> euro_to_cent('0.01')
    1
    >>> euro_to_cent('0.001')
    0
    """

    value = decimal.Decimal(amount) * 100
    return coerce(value.quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_DOWN))


def netto(amount, tax=19):
    """
    Mehrwertsteuer aus den Preisen rausrechnen.

    >>> netto(decimal.Decimal('1.19'))
    Decimal('1.00')
    >>> netto(decimal.Decimal('1.08'), tax=8)
    Decimal('1.00')
    >>> netto(decimal.Decimal('1812'), tax=3)
    Decimal('1759.22')
    """

    tax = decimal.Decimal(str(tax))

    if tax >= 100:
        raise ValueError('tax must not be greater than 100%')

    percent = amount / (decimal.Decimal(100) + tax)
    amount = percent * 100
    return amount.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_DOWN)


def brutto(amount, tax=19):
    """
    Mehrwertsteuer zu den Preisen rechnen.

    >>> brutto(decimal.Decimal('1.00'))
    Decimal('1.19')
    >>> brutto(decimal.Decimal('1.00'), tax=8)
    Decimal('1.08')
    >>> brutto(decimal.Decimal('5711'), tax=23)
    Decimal('7024.53')
    """

    tax = decimal.Decimal(str(tax))

    if tax >= 100:
        raise ValueError("tax must not be greater than 100%")

    percent = amount / decimal.Decimal(100)
    amount = percent * (100 + tax)
    return amount.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_DOWN)


def tara(amount, tax=19):
    """
    Rechne die Differenz zwischen Brutto- und Nettopreis aus.

    >>> tara(decimal.Decimal('1.19'))
    Decimal('0.19')
    >>> tara(decimal.Decimal('1.05'), tax=5)
    Decimal('0.05')
    """

    tax = decimal.Decimal(str(tax))

    if tax >= 100:
        raise ValueError('tax must not be greater than 100%')

    return amount - netto(amount, tax=tax)


def spanne(verkaufspreis, selbstkosten, tax=19):
    """Berechne die Gewinnspanne für einen Verkaufspreis und einen Selbstkostenanteil"""

    verkaufspreis = decimal.Decimal(str(verkaufspreis))
    selbstkosten = decimal.Decimal(str(selbstkosten))
    nettopreis = netto(verkaufspreis, tax=tax)
    return (nettopreis - selbstkosten) / nettopreis


if __name__ == "__main__":
    import doctest
    doctest.testmod()
