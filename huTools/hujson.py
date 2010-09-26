#!/usr/bin/env python
# encoding: utf-8
"""
hujson.py - extended json - tries to be compatible with simplejson

hujson can encode additional types like decimal and datetime into valid json.
All the heavy lifting is done by John Millikin's `jsonlib`.

Created by Maximillian Dornseif on 2010-09-10.
Copyright (c) 2010 HUDORA. All rights reserved.
"""


from _jsonlib import UnknownSerializerError
import _jsonlib
import datetime


def _unknown_handler(value):
    if isinstance(value, datetime.date):
        return str(value)
    elif isinstance(obj, datetime.datetime):
        return value.isoformat() + 'Z'
    raise UnknownSerializerError


def dumps(val):
    return _jsonlib.write(val, on_unknown=_unknown_handler)
