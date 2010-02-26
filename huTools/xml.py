#!/usr/bin/env python
# encoding: utf-8
"""
xml.py

Created by Christian Klein on 2010-02-26.
Copyright (c) 2010 HUDORA GmbH. All rights reserved.
"""

import datetime

def encode_text(input):
    """Encode for usage in XML Tree"""
    
    if isinstance(input, str):
        return attr.decode('utf-8', 'replace')
    elif isinstance(input, datetime.datetime):
        if not(input.hour or input.minute):
            fmt = '%Y-%m-%d'
        else:
            fmt = '%Y-%m-%d %H:%M'
        return input.strftime(fmt)
    else:
        return unicode(input)