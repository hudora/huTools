#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2007 HUDORA GmbH. BSD Licensed.
"""

import doctest
import sys
from types import StringType

__revision__ = "$Revision$"


def deUTF8(data):
    """This is meant to help with utf-8 data appearing where unicode should apperar."""
    # In particular my DB is returning the wrong thing.
    if type(data) == StringType:
        return data.decode('utf-8')
    return data
    

# native, HTML, default Unicode (Code page 850), Unicode combined Character, Windows-1250
_recodings = {'ae': set(['ä', u'ä', '&auml;', '\u00E4', u'\u00E4', '\u0308a', '\xc3\xa4']),
              'oe': set(['ö', u'ö', '&ouml;', '\u00F6', u'\u00F6', '\u0308o', '\xc3\xb6']),
              'ue': set(['ü', u'ü', '&uuml;', '\u00FC', u'\u00FC', '\u0308u', '\xc3\xbc']),
              'Ae': set(['Ä', u'Ä', '&Auml;', '\u00C4', u'\u00C4', '\u0308A', '\xc3\x84']),
              'Oe': set(['Ö', u'Ö', '&Ouml;', '\u00D6', u'\u00D6', '\u0308O', '\xc3\x96']),
              'Ue': set(['Ü', u'Ü', '&Uuml;', '\u00DC', u'\u00DC', '\u0308U', '\xc3\x9c']),
              'ss': set(['ß', u'ß', '&szlig;', '\u00DF', u'\u00DF', '\xc3\x9f']),
              'e': set(['é', u'é', '\xc3\xa9']),
             }


def deUmlaut(data):
    """Converts a text to ASCII acting smart about Umlauts.
    
    >>> deUmlaut('1 Über Hügel saß René äöüÄÖÜß')
    '1 Ueber Huegel sass Rene aeoeueAeOeUess'
    """
    
    for to_char, from_chars in _recodings.items():
        for from_char in from_chars:
            try:
                data = data.replace(from_char, to_char)
            except UnicodeDecodeError:
                data = data
    try:
        return data.encode('ascii', 'replace')
    except UnicodeEncodeError, msg:
        raise ValueError('%s: %r' % (msg, data))
    except UnicodeDecodeError, msg:
        raise ValueError('%s: %r' % (msg, data))
    

if __name__ == '__main__':
    failure_count, test_count = doctest.testmod()
    sys.exit(failure_count)
