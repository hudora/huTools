#!/usr/bin/env python
# encoding: utf-8
"""
engine_httplib2.py implements httplib2 based queries for huTools.http

Created by Maximillian Dornseif on 2010-10-24.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import socket
from huTools.http import exceptions
_http = None


def request(url, method, content, headers, timeout=15):
    """Does a HTTP Request via httplib2 service."""

    global _http
    if not _http:
        import huTools.http._httplib2
        _http = huTools.http._httplib2.Http(timeout=timeout)

    headers['User-Agent'] = headers.get('User-Agent', '') + ' (httplib2)'

    # Do not re-use the global Http object after a timeout.
    # To achieve this, it is set to None.
    try:
        resp, content = _http.request(url, method, content, headers=headers)
    except socket.timeout:
        _http = None
        raise exceptions.Timeout

    replyheaders = {}
    replyheaders.update(resp)
    return int(resp.status), replyheaders, content
