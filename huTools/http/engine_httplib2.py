#!/usr/bin/env python
# encoding: utf-8
"""
engine_httplib2.py implements httplib2 based queries for huTools.http

Created by Maximillian Dornseif on 2010-10-24.
Copyright (c) 2010, 2011 HUDORA. All rights reserved.
"""

import socket
import huTools.http.tools
from huTools.http import exceptions
_http = None


def request(url, method, content, headers, timeout=50, caching=None):
    """Does a HTTP Request via httplib2."""
    global _http
    if not _http:
        import huTools.http._httplib2
        _http = huTools.http._httplib2.Http(timeout=timeout)

    headers['User-Agent'] = headers.get('User-Agent', '') + ' (httplib2)'
    _http.clear_credentials()
    _http.forward_authorization_headers = True
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


class AsyncHttpResult(object):
    """Syncronous emulation for plain Python.

    See `engine_appengine.AsyncHttpResult()` for the thinking behind it.
    `huTools.http.fetch_async()` is a somewhat more high-level interface.
    """

    def __init__(self, caching=None):
        self.url, self.method, self.content, self.headers, self.timeout = None, None, None, None, None
        self._result = None

    def fetch(self, url, content='', method='GET', credentials=None, headers=None, multipart=False, ua='',
              timeout=25, returnhandler=lambda x, y, z: (x, y, z)):
        """Save parameters but delay request execution until get_result() is called."""
        self.url, self.method, self.content, self.headers, self.timeout, _dummy = \
            huTools.http.tools.prepare_headers(url, content, method, credentials, headers, multipart,
                                               ua, timeout)
        self.returnhandler = returnhandler

    def get_result(self):
        """Execute request pass it to returnhandler and return."""
        # Cache the result because we mght get called more than once
        if not self._result:
            self._result = self.returnhandler(*request(self.url, self.method, self.content,
                                                       self.headers, self.timeout))
        return self._result
