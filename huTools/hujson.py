#!/usr/bin/env python
# encoding: utf-8
"""
hujson.py - extended json - tries to be compatible with simplejson

hujson can encode additional types like decimal and datetime into valid json.
All the heavy lifting is done by John Millikin's `jsonlib`, see
https://launchpad.net/jsonlib

Created by Maximillian Dornseif on 2010-09-10.
Copyright (c) 2010 HUDORA. All rights reserved.
"""


from _jsonlib import UnknownSerializerError
import _jsonlib
import datetime


def _unknown_handler(value):
    if isinstance(value, datetime.date):
        return str(value)
    elif isinstance(value, datetime.datetime):
        return value.isoformat() + 'Z'
    elif hasattr(value, 'properties'):
        return dict([(key, getattr(value, key)) for key in value.properties().keys()])
    elif 'google.appengine.api.users.User' in str(type(value)):
        return "%s/%s" % (value.user_id(), value.email())
    elif 'google.appengine.api.datastore_types.Key' in str(type(value)):
        return str(value)
    raise UnknownSerializerError("%s(%s)" % (type(value), value))


def dumps(val, indent=' '):
    return _jsonlib.write(val, on_unknown=_unknown_handler, indent=indent)


def loads(data):
    return _jsonlib.read(data)
