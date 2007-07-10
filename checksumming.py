#!/usr/bin/env python
# encoding: utf-8

"""
checksumming.py - various checksum functions.

Created by Maximillian Dornseif on 2006-11-05.

This file can be used under an BSD License.
"""

__revision__ = "$Revision$"

import doctest, unittest

# The original code came from QBasic code I written from the EAN-Spec in 1986 or so.
# The Python code was inspired by bookland.py and was extended to "longer than EAN"
# by checking the javascript at 
# http://www.gs1.org/productssolutions/barcodes/support/check_digit_calculator.html
def ean_digit(arg):
    """Calculate UPCA/EAN13/NVE checksum for any given string consiting of an arbitary number of digits.
    
    >>> ean_digit('400599871650')
    '2'
    >>> ean_digit('34005998000000027')
    '5'
    """
    
    factor = 3
    summe = 0
    for index in range(len(arg)-1, -1, -1):
        summe += int(arg[index]) * factor
        factor = 4 - factor
    return str((10 - (summe % 10)) % 10)


def _ean_digit2(arg):
    """Alternate EAN check digit calculation used for sanity checks."""
    if len(arg) % 2 == 1:
        weight = [3, 1] * ((len(arg) * 2) + 1)
    else:
        weight = [1, 3] * ((len(arg) * 2) + 1)
    magic = 10
    summe = 0
    for i in range(len(arg)):         # checksum based on first 12 digits.
        summe = summe + int(arg[i]) * weight[i]
    ret = ( magic - (summe % magic) ) % magic
    if ret < 0 or ret >= magic:
        raise RuntimeError, "EAN checkDigit: something wrong."
    return str(ret)

def dpd_digit(arg):
    """Calculates the Checksum for DPD Packets.
    
    See http://static.23.nu/md/Pictures/BIC3_DPDPaketscheinspez_Neu_D_v101.pdf page 22 for an explanation.
    
    Exaple:
    >>> dpd_digit('400599871650')
    'E'
    >>> dpd_digit('007110601632532948375179276')
    'A'
    """

    # to calculate the code values - position equals code value
    _chartable = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    mod = 36
    cd = mod
    for char in arg:
        cd = cd + _chartable.index(char.upper())
        if cd > mod:
            cd = cd - mod
        cd = 2 * cd
        if cd > mod:
            cd = cd - mod - 1
    cd = mod + 1 - cd
    if cd == mod:
        cd = 0
    return _chartable[cd]


# test cases

class EanTests(unittest.TestCase):
    """Simple Tests for EAN checkdigit calculation."""
    def test_ean_digit1(self):
        """Test known EANs and their checksumms."""
        self.assertEqual(ean_digit(''), '0')
        self.assertEqual(ean_digit('2'), '4')
        self.assertEqual(ean_digit('22'), '2')
        self.assertEqual(ean_digit('222'), '6')
        self.assertEqual(ean_digit('1234567'), '0')
        self.assertEqual(ean_digit('12345678901'), '2')
        self.assertEqual(ean_digit('062235652032'), '4')
        self.assertEqual(ean_digit('978014200057'), '1')
        self.assertEqual(ean_digit('400599871650'), '2')
        self.assertEqual(ean_digit('400599899379'), '8')
        self.assertEqual(ean_digit('1234567890123'), '1')
        self.assertEqual(ean_digit('0000001234567'), '0')
        self.assertEqual(ean_digit('0012345678901'), '2')
        self.assertEqual(ean_digit('0123456789012'), '8')
        self.assertEqual(ean_digit('00000000000000000'), '0')
        self.assertEqual(ean_digit('00000000000000001'), '7')
        self.assertEqual(ean_digit('00000000000000010'), '9')
        self.assertEqual(ean_digit('00000000000000100'), '7')
        self.assertEqual(ean_digit('12345678901234567'), '5')
        self.assertEqual(ean_digit('22222222222222222'), '0')
        self.assertEqual(ean_digit('99999999999999999'), '5')
        self.assertEqual(ean_digit('34005998000000026'), '8')
        self.assertEqual(ean_digit('34005998000000027'), '5')
        self.assertEqual(ean_digit('34005998000000028'), '2')
        self.assertEqual(ean_digit('34005998000000028'), '2')
        self.assertEqual(ean_digit('99999999999999999'), '5')
        self.assertEqual(ean_digit('999999999999999999'), '6')
        self.assertEqual(ean_digit('9999999999999999999'), '9')
        self.assertEqual(ean_digit('99999999999999999999'), '0')
        self.assertEqual(ean_digit('999999999999999999999'), '3')
        self.assertEqual(ean_digit('9999999999999999999999'), '4')
        self.assertEqual(ean_digit('99999999999999999999999'), '7')
        self.assertEqual(ean_digit('999999999999999999999999'), '8')
        self.assertEqual(ean_digit('9999999999999999999999999'), '1')
        self.assertEqual(ean_digit('99999999999999999999999999'), '2')
        self.assertEqual(ean_digit('999999999999999999999999999'), '5')
        self.assertEqual(ean_digit('9999999999999999999999999999'), '6')
        self.assertEqual(ean_digit('99999999999999999999999999999'), '9')
        self.assertEqual(ean_digit('999999999999999999999999999999'), '0')
        self.assertEqual(ean_digit('9999999999999999999999999999999'), '3')
        self.assertEqual(ean_digit('99999999999999999999999999999999'), '4')
        self.assertEqual(ean_digit('999999999999999999999999999999999'), '7')
        self.assertEqual(ean_digit('9999999999999999999999999999999999'), '8')
        self.assertEqual(ean_digit('99999999999999999999999999999999999'), '1')
        self.assertEqual(ean_digit('999999999999999999999999999999999999'), '2')
        self.assertEqual(ean_digit('9999999999999999999999999999999999999'), '5')
        self.assertEqual(ean_digit('99999999999999999999999999999999999999'), '6')
        self.assertEqual(ean_digit('999999999999999999999999999999999999999'), '9')
        self.assertEqual(ean_digit('9999999999999999999999999999999999999999'), '0')
        self.assertEqual(ean_digit('99999999999999999999999999999999999999999'), '3')
        self.assertEqual(ean_digit('999999999999999999999999999999999999999999'), '4')
        self.assertEqual(ean_digit('9999999999999999999999999999999999999999999'), '7')
        self.assertEqual(ean_digit('99999999999999999999999999999999999999999999'), '8')
        self.assertEqual(ean_digit('999999999999999999999999999999999999999999999'), '1')
        self.assertEqual(ean_digit('9999999999999999999999999999999999999999999999'), '2')
        self.assertEqual(ean_digit('99999999999999999999999999999999999999999999999'), '5')
        self.assertEqual(ean_digit('999999999999999999999999999999999999999999999999'), '6')
        self.assertEqual(ean_digit('9999999999999999999999999999999999999999999999999'), '9')
        self.assertEqual(ean_digit('99999999999999999999999999999999999999999999999999'), '0')
        self.assertEqual(ean_digit('999999999999999999999999999999999999999999999999999'), '3')
        self.assertEqual(ean_digit('9999999999999999999999999999999999999999999999999999'), '4')
        self.assertEqual(ean_digit('99999999999999999999999999999999999999999999999999999'), '7')
        self.assertEqual(ean_digit('999999999999999999999999999999999999999999999999999999'), '8')
        self.assertEqual(ean_digit('9999999999999999999999999999999999999999999999999999999'), '1')
        self.assertEqual(ean_digit('99999999999999999999999999999999999999999999999999999999'), '2')
        self.assertEqual(ean_digit('999999999999999999999999999999999999999999999999999999999'), '5')
        self.assertEqual(ean_digit('9999999999999999999999999999999999999999999999999999999999'), '6')
        self.assertEqual(ean_digit('99999999999999999999999999999999999999999999999999999999999'), '9')
        self.assertEqual(ean_digit('999999999999999999999999999999999999999999999999999999999999'), '0')
        self.assertEqual(ean_digit('9999999999999999999999999999999999999999999999999999999999999'), '3')
        self.assertEqual(ean_digit('99999999999999999999999999999999999999999999999999999999999999'), '4')

    def test_ean_digit2(self):
        """Test the backup EAN calculation function."""
        self.assertEqual(_ean_digit2(''), '0')
        self.assertEqual(_ean_digit2('1234567'), '0')
        self.assertEqual(_ean_digit2('12345678901'), '2')
        self.assertEqual(_ean_digit2('062235652032'), '4')
        self.assertEqual(_ean_digit2('978014200057'), '1')
        self.assertEqual(_ean_digit2('400599871650'), '2')
        self.assertEqual(_ean_digit2('400599899379'), '8')
        self.assertEqual(_ean_digit2('1234567890123'), '1')
        self.assertEqual(_ean_digit2('0000001234567'), '0')
        self.assertEqual(_ean_digit2('0012345678901'), '2')
        self.assertEqual(_ean_digit2('0123456789012'), '8')
        self.assertEqual(_ean_digit2('00000000000000000'), '0')
        self.assertEqual(_ean_digit2('00000000000000001'), '7')
        self.assertEqual(_ean_digit2('00000000000000010'), '9')
        self.assertEqual(_ean_digit2('00000000000000100'), '7')
        self.assertEqual(_ean_digit2('12345678901234567'), '5')
        self.assertEqual(_ean_digit2('22222222222222222'), '0')
        self.assertEqual(_ean_digit2('99999999999999999'), '5')
        self.assertEqual(_ean_digit2('34005998000000026'), '8')
        self.assertEqual(_ean_digit2('34005998000000027'), '5')
        self.assertEqual(_ean_digit2('34005998000000028'), '2')

class DPDTests(unittest.TestCase):
    def test_checkdigit(self):
        self.assertEqual(dpd_digit(''), '1')
        self.assertEqual(dpd_digit('2'), 'X')
        self.assertEqual(dpd_digit('22'), 'P')
        self.assertEqual(dpd_digit('01632532948375'), '2')
        self.assertEqual(dpd_digit('007110601632532948375179276'), 'A')
        self.assertEqual(dpd_digit('007110601632532948375101276'), 'O')
        self.assertEqual(dpd_digit('007110601631234567890136276'), '0')
        self.assertEqual(dpd_digit('09445008454226'), 'K')
        self.assertEqual(dpd_digit('09445008454227'), 'I')
        self.assertEqual(dpd_digit('00711060163123456789013627699999999999999999999999999999'), 'O')
        self.assertEqual(dpd_digit('0071106016312345678901362769999999999999999999999999999999'), '5')
        
    
if __name__ == '__main__':
    doctest.testmod()
    unittest.main()
