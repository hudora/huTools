#!/usr/bin/env python
# encoding: utf-8
"""
engine_appengine.py implements urlfetch based queries for huTools.http.

See http://code.google.com/appengine/docs/python/urlfetch/overview.html for the basics of the
AppEngine capabilities.

Created by Maximillian Dornseif on 2010-10-24.
Copyright (c) 2010, 2011 HUDORA. All rights reserved.
"""


import huTools.http.tools
import logging
import os
from google.appengine.api.urlfetch import create_rpc, make_fetch_call
from google.appengine.api import memcache, urlfetch, urlfetch_errors
from huTools.http import exceptions


# this needs SDK 1.5.3
urlfetch.set_default_fetch_deadline(50)


def request(url, method, content, headers, timeout=50, caching=None):
    """Does a HTTP Request via Google Appengine urlfetch Service.

    If you give an integer value as `caching` parameter, the results are cached for that time and
    subsequent fetches will be served from the cache.
    """

    cachekey = "_hutools%s.http_%s_%s_%s_%s" % (os.environ.get('CURRENT_VERSION_ID', ''), method, url,
                                                hash(content), hash(tuple(headers.items())))
    if caching:
        # try to read result from memcache
        ret = memcache.get(cachekey)
        if ret:
            return ret  # cache hit we are done

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
    ret = (int(result.status_code), result.headers, result.content)
    if caching:
        memcache.set(cachekey, ret, caching)
    return ret


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

    If you give an integer value as `caching` parameter, the results are cached for that time and
    subsequent fetches will be served from the cache.
    """

    def __init__(self, caching=None):
        # _resultcache is used so get_result() can be called more than once.
        self._resultcache = None
        self._caching = caching

    def fetch(self, url, content='', method='GET', credentials=None, headers=None, multipart=False, ua='',
              timeout=50, returnhandler=lambda x, y, z: (x, y, z)):
        """Initiate fetch call."""
        url, method, content, headers, timeout, _dummy = huTools.http.tools.prepare_headers(url,
            content, method, credentials, headers, multipart, ua, timeout)
        self._cachekey = "_hutools%s.http.async_%s_%s_%s_%s" % (os.environ.get('CURRENT_VERSION_ID', ''),
                                                                method, url, hash(content),
                                                                hash(tuple(headers.items())))
        self.returnhandler = returnhandler

        if self._caching:
            # try to read result from memcache
            self._resultcache = memcache.get(self._cachekey)
            if self._resultcache:
                logging.info("resultcache for during fetch %s:", self._cachekey)
                return  # cache hit we are done

        # Cache miss or no cache wanted, do wait for the real http fetch
        self.rpc = create_rpc(deadline=timeout)
        logging.info('fetching (async) %r %r', method, url)
        make_fetch_call(self.rpc, url, content, method, headers)

    def get_result(self):
        """Wait until request is done, pass results to returnhandler and return to caller."""
        # we cache the result in place to ensure, that calling `get_result()` twice does not mix thing up
        if not self._resultcache:
            if self._caching:
                # try to read result from memcache
                self._resultcache = memcache.get(self._cachekey)
                if self._resultcache:
                    logging.info("resultcache for %s:", self._cachekey)
                    logging.info(self._resultcache)
                    return self._resultcache
            # Cache miss or no cache wanted, do wait for the real http fetch
            result = self.rpc.get_result()
            self._resultcache = self.returnhandler(result.status_code, result.headers, result.content)
            if self._caching:
                memcache.set(self._cachekey, self._resultcache, self._caching)
        logging.info("final resultcache for %s:", self._cachekey)
        logging.info(self._resultcache)
        return self._resultcache
