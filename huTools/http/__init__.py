#!/usr/bin/env python
# encoding: utf-8
"""
huTools/http/__init__.py

Provides a simple interface for doing HTTP requests on stock Python and on Google Appengine. Provides
unicode aware application/x-www-form-urlencoded encoding and an do multipart/form-data (file upload)
without aditional code. On Google Appengine it incerass the timeout from 5 seconds to 10.

Usage is without suprises::

    >>> status, header, body = fetch('http://www.postbin.org/o0ds54',
                                     {'küh': 'Iñtërnâtiônàlizætiøn', 'just a test': 212},
                                     headers={'X-Foo': 'Bar'})

File Upload just works::

    >>> status, header, body = fetch('http://www.postbin.org/o0ds54',
                                     {'hosts': open('/etc/hosts', 'r')}, 'POST')

`fetch2xx()` throws a `WrongStatusCode` if the server returns a status code outside the 200-299 range.
`fetch_json2xx()` in addition decodes a JSON reply and returns that.
"""

from huTools.http.base import *
