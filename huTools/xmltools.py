#!/usr/bin/env python
# encoding: utf-8
"""
xmltools.py

Created by Christian Klein on 2010-02-26.
Copyright (c) 2010 HUDORA GmbH. All rights reserved.
"""

import datetime
import xml.etree.ElementTree as ET


def encode_text(data):
    """
    Encode for usage in XML Tree
    
    >>> encode_text(None)
    u''
    >>> encode_text('Alex')
    u'Alex'
    >>> encode_text(u'Alex')
    u'Alex'
    >>> encode_text(12)
    u'12'
    >>> encode_text(callable(encode_text))
    u'True'
    >>> encode_text(callable)
    u''
    """
    
    if callable(data):
        try:
            return encode_text(data())
        except TypeError:
            return u''
    
    if isinstance(data, str):
        return data.decode('utf-8', 'replace')
    elif isinstance(data, datetime.datetime):
        if not(data.hour or data.minute):
            fmt = '%Y-%m-%d'
        else:
            fmt = '%Y-%m-%d %H:%M'
        return data.strftime(fmt)
    elif data is None:
        return u''
    else:
        return unicode(data)


def add_fields(root, source, fieldnames):
    """
    Add a number of fields to a XML Tree.
    """
    for fieldname in fieldnames:
        elem = ET.SubElement(root, fieldname)
        if hasattr(source, fieldname):
            elem.text = encode_text(getattr(source, fieldname, ''))
    return root


if __name__ == "__main__":
    import doctest
    doctest.testmod()