#!/usr/bin/env python
# encoding: utf-8
"""
humessaging.py - tools for creating and halndling Messages complying with the Hudora Message Format.

The HUDORA Message format is a set of simple conventions to format messages in a
message system agnostic way. Messages are encoded in JSON.

Created by Maximillian Dornseif on 2009-07-29.
Copyright (c) 2009 HUDORA. All rights reserved.
"""

import decimal
import huTools.calendar.formats
import huTools.luids
import re
import simplejson as json


def extend_audittrail(audit_info='', audit_trail=''):
    """Append audit_info to audit_trail.
    
    >>> extend_audittrail()
    ''
    >>> extend_audittrail('a;a')
    'a a'
    >>> extend_audittrail('b;b', 'a a')
    'a a;b b'
    """
    return ';'.join([x for x in audit_trail.split(';') + [audit_info.replace(';', ' ')] if x])
    

def empty_message(creator, audit_info='', audit_trail='', guid=''):
    """Returns an empty message template following the huMessaging Standard.
    
    creator:     user (prefered) or library tool which created the message. Suitable for audit messages.
                 Example: "Maximillian Dornseif via cs.zwitscher/r3456"
    audit_info:  a human readable description of the processing stage.
                 Example: "flagged as problematic by nachschieber.py"
    audit_trail: semicolen sparated list of previous processing stages.
    guid:        Unique id of this message. Should never repeat. Generate by something unique for your
                 processing step. E.g. "lieferschenrueckmeldung-4234543". Should only contain
                 printable ASCII characters.
    """
    ret = {'created_at': huTools.calendar.formats.rfc3339_date(),
           'created_by': creator,
           'audit_trail': audit_trail,
           'guid': guid,
          }
    if audit_info:
        ret['audit_trail'] = extend_audittrail(audit_info, audit_trail)
    else:
        ret['audit_trail'] = extend_audittrail('send via %s' % creator, audit_trail)
    if not guid:
        ret['guid'] = 'msg-%s' % huTools.luids.guid128(salt=audit_info)
    return ret
    

def _encode_decimal(obj):
    """Helper for encoding decimal objects. Needs later fixup by regular expressions.
    
    >>> _encode_decimal(decimal.Decimal('5.00'))
    'Decimal("5.00")'
    """
    if isinstance(obj, decimal.Decimal):
        return repr(obj)
    raise TypeError("%r is not JSON serializable" % (obj, ))
    

_decimal_re = re.compile(r'"Decimal\(.+"(\d+)\.(\d+).+"\)"')


def encode(message):
    """Decode the dict-like message into a valid wire representation.
    
    Besides the types familar from Python's json module it can serialize Decimal() objects.
    
    >>> encode({'guid': 123, 'created_by': 'test', 'num': decimal.Decimal('5.00')})
    '{"created_by":"test","guid":123,"num":5.00}'
    """
    assert 'created_by' in message
    assert 'guid' in message
    ret = json.dumps(message, default=_encode_decimal, sort_keys=True, separators=(',', ':'))
    # replace "Decimal(\\"5.00\\")" with 5.00
    return re.sub(_decimal_re, r'\1.\2', ret)
    

def decode(data):
    """
    Decode a message from a valid wire representation.
    
    Besides the types familar from Python's json module it can unserialize Decimal() objects.
    
    >>> decode('{"created_by":"test","guid":123,"num":5.00}')
    {'guid': 123, 'num': Decimal("5.00"), 'created_by': 'test'}
    """
    return json.loads(data, parse_float=decimal.Decimal)
    

def setup_queue(chan, name, durable=False, auto_delete=False, exclusive=False):
    """Sets up AMQP Queue 'name' and the assorted exchange, routing key and stuff dictated by AMQP"""
    
    chan.exchange_declare(exchange=name, type="direct", durable=durable, auto_delete=auto_delete)
    chan.queue_declare(queue=name, durable=durable, exclusive=exclusive, auto_delete=auto_delete)
    chan.queue_bind(queue=name, exchange=name, routing_key=name)
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()
