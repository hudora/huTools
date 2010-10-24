#!/usr/bin/env python
# encoding: utf-8
"""
tools.py

Created by Maximillian Dornseif on 2010-10-24.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import urllib
from poster_encode import multipart_encode
import urlparse


# quoting based on
# http://svn.python.org/view/python/branches/release27-maint/Lib/urllib.py?view=markup&pathrev=82940
# by Matt Giuca
always_safe = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
               'abcdefghijklmnopqrstuvwxyz'
               '0123456789' '_.-')
_safe_map = {}
for i, c in zip(xrange(256), str(bytearray(xrange(256)))):
    _safe_map[c] = c if (i < 128 and c in always_safe) else ('%%%02X' % i)
_safe_quoters = {}


def quote(s, safe='/', encoding=None, errors=None):
    """quote('abc def') -> 'abc%20def'

    Each part of a URL, e.g. the path info, the query, etc., has a
    different set of reserved characters that must be quoted.

    RFC 2396 Uniform Resource Identifiers (URI): Generic Syntax lists
    the following reserved characters.

    reserved    = ";" | "/" | "?" | ":" | "@" | "&" | "=" | "+" |
                  "$" | ","

    Each of these characters is reserved in some component of a URL,
    but not necessarily in all of them.

    By default, the quote function is intended for quoting the path
    section of a URL.  Thus, it will not encode '/'.  This character
    is reserved, but in typical usage the quote function is being
    called on a path where the existing slash characters are used as
    reserved characters.

    string and safe may be either str or unicode objects.

    The optional encoding and errors parameters specify how to deal with the
    non-ASCII characters, as accepted by the unicode.encode method.
    By default, encoding='utf-8' (characters are encoded with UTF-8), and
    errors='strict' (unsupported characters raise a UnicodeEncodeError).
    """
    # fastpath
    if not s:
        return s

    if encoding is not None or isinstance(s, unicode):
        if encoding is None:
            encoding = 'utf-8'
        if errors is None:
            errors = 'strict'
        s = s.encode(encoding, errors)
    if isinstance(safe, unicode):
        # Normalize 'safe' by converting to str and removing non-ASCII chars
        safe = safe.encode('ascii', 'ignore')

    cachekey = (safe, always_safe)
    try:
        (quoter, safe) = _safe_quoters[cachekey]
    except KeyError:
        safe_map = _safe_map.copy()
        safe_map.update([(c, c) for c in safe])
        quoter = safe_map.__getitem__
        safe = always_safe + safe
        _safe_quoters[cachekey] = (quoter, safe)
    if not s.rstrip(safe):
        return s
    return ''.join(map(quoter, s))


def quote_plus(s, safe='', encoding=None, errors=None):
    """Quote the query fragment of a URL; replacing ' ' with '+'"""
    if ' ' in s:
        s = quote(s, safe + ' ', encoding, errors)
        return s.replace(' ', '+')
    return quote(s, safe, encoding, errors)


def urlencode(query):
    """Encode a sequence of two-element tuples or dictionary into a URL query string.

    If the query arg is a sequence of two-element tuples, the order of the
    parameters in the output will match the order of parameters in the
    input.
    """

    if hasattr(query, 'items'):
        # mapping objects
        query = query.items()
    l = []
    for k, v in query:
        k = quote_plus(k)
        if isinstance(v, basestring):
            v = quote_plus(v)
            l.append(k + '=' + v)
        else:
            v = quote_plus(unicode(v))
            l.append(k + '=' + v)
    return '&'.join(l)
