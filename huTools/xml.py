#!/usr/bin/env python
# encoding: utf-8
"""
xml.py

Created by Christian Klein on 2010-02-26.
Copyright (c) 2010 HUDORA GmbH. All rights reserved.
"""

import datetime

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
    else:
        return unicode(input)
