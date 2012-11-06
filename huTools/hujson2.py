#!/usr/bin/env python
# encoding: utf-8
"""
hujson.py - extended json - tries to be compatible with simplejson

hujson can encode additional types like decimal and datetime into valid json.

Created by Maximillian Dornseif on 2010-09-10.
Copyright (c) 2010, 2012 HUDORA. All rights reserved.
"""
import datetime
import decimal
import json


def _unknown_handler(value):
    """Helfer für json.dmps()) - stammt aus hujson"""
    if isinstance(value, datetime.date):
        return str(value)
    elif isinstance(value, datetime.datetime):
        return value.isoformat() + 'Z'
    elif isinstance(value, decimal.Decimal):
        return unicode(value)
    elif hasattr(value, 'properties') and callable(value.properties):
        return dict([(key, getattr(value, key)) for key in value.properties().keys()])
    elif 'google.appengine.api.users.User' in str(type(value)):
        return "%s/%s" % (value.user_id(), value.email())
    elif 'google.appengine.api.datastore_types.Key' in str(type(value)):
        return str(value)
    elif hasattr(value, 'as_dict') and callable(value.as_dict):
        # helpful for structured.Struct() Objects
        return value.as_dict()
    elif hasattr(value, 'dict_mit_positionen') and callable(value.dict_mit_positionen):
        # helpful for our internal data-modelling
        return value.dict_mit_positionen()
    raise TypeError("%s(%s)" % (type(value), value))


def dumps(val, indent=' '):
    return json.dumps(val, sort_keys=True, indent=bool(indent), ensure_ascii=True,
                      default=_unknown_handler)


def loads(data):
    return json.loads(data)
