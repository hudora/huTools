#!/usr/bin/env python
# encoding: utf-8
"""
xml.py

Created by Christian Klein on 2010-02-26.
Copyright (c) 2010 HUDORA GmbH. All rights reserved.
"""

import datetime
import xml.etree.ElementTree as ET


def encode_text(data):
    """Encode for usage in XML Tree"""

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
