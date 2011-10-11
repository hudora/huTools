#!/usr/bin/env python
# encoding: utf-8
"""
engine_appengine.py implements urlfetch based queries for huTools.http.

See http://code.google.com/appengine/docs/python/urlfetch/overview.html for the basics of the
AppEngine capabilities.

Created by Maximillian Dornseif on 2010-10-24.
Copyright (c) 2010, 2011 HUDORA. All rights reserved.
"""


import logging
import huTools.http.tools
from google.appengine.api.urlfetch import create_rpc, make_fetch_call
from google.appengine.api import urlfetch, urlfetch_errors
from huTools.http import exceptions


# this needs SDK 1.5.3
urlfetch.set_default_fetch_deadline(50)


def request(url, method, content, headers, timeout=50):
    """Does a HTTP Request via Google Appengine urlfetch Service.

    Incereases the default appengine timeout from 5 seconds to 50.
    (For Web-Requests this is reduced to 10s by the GAE Infrastructure)"""

    # on appengine debuging is always post mortem, so better log what we arde doing
    logging.debug('fetching %r %r', method, url)
    if method == 'GET':
        method = urlfetch.GET
    elif method == 'POST':
        method = urlfetch.POST
    elif method == 'DELETE':
        method = urlfetch.DELETE
    elif method == 'PUT':
        method = urlfetch.PUT
    elif method == 'HEAD':
        method = urlfetch.HEAD
    headers['User-Agent'] = headers.get('User-Agent', '') + ' (urlfetch)'
    try:
        result = urlfetch.fetch(url=url, deadline=timeout, payload=content, method=method, headers=headers)
    except urlfetch_errors.DownloadError, exception:
        # App Engine uses the same exception class for several types of errors.
        # It seems that the only mean to distinguish timeouts from other errors
        # is by looking at the error message.
        # This may break when error messages change. In that case, the exception is re-raised.
        if 'timed out' in str(exception):
            raise exceptions.Timeout
        else:
            raise
    return int(result.status_code), result.headers, result.content


# Es folgt  Implementierung eines Asyncronen Interfaces zu `huTools.http.fetch()` [LH#1181]
class AsyncHttpResult(object):
    """Starts a asyncronenous requests and processes the result.

    >>> o = _AsyncHttpResult()
    >>> o.fetch(url, credentials='u:p', ua='cs.masterdata.eaplight',
                headers={'accept': 'application/json'}, returnhandler=returnhandler)

    `fetch()` has the same signature as `huTools.http.fetch()` with the additional `returnhandler`
    parameter. `returnhandler` has the signature `(status, headers, content)`. It's returnvalue is
    returned to the caller of `o.get_result()`. The following is equivalent to a syncronous
    fetch:

    >>> o = AsyncHttpResult()
    >>> o.fetch(url, returnhandler=lambda x, y, z: (x, y, z))
    >>> o.get_result()

    A typical usage in a library might look like this:

        def get_eap_async(artnr):
            def returnhandler(status, headers, content):
                if status == 200:
                    return json.loads(content)
                else:
                    raise RuntimeError("%d: %s" % (status, content))

            o = _AsyncHttpResult()
            o.fetch('http://example.com/foo', returnhandler=returnhandler)
            return o

    Callers could now use
        >>> get_eap_async(artnr).get_result()

    `huTools.http.fetch_async()` is a somewhat more high-level interface.
    """

    def __init__(self):
        # _resultcache is used so get_result() can be called more than once.
        self._resultcache = None

    def fetch(self, url, content='', method='GET', credentials=None, headers=None, multipart=False, ua='',
              timeout=50, returnhandler=lambda x, y, z: (x, y, z)):
        """Initiate fetch call."""
        url, method, content, headers, timeout = huTools.http.tools.prepare_headers(url,
            content, method, credentials, headers, multipart, ua, timeout)
        self.returnhandler = returnhandler
        self.rpc = create_rpc(deadline=timeout)
        logging.info('fetching (async) %r %r', method, url)
        make_fetch_call(self.rpc, url, content, method, headers)

    def get_result(self):
        """Wait until request is done, pass results to returnhandler and return to caller."""
        if not self._resultcache:
            result = self.rpc.get_result()
            self._resultcache = self.returnhandler(result.status_code, result.headers, result.content)
        return self._resultcache
