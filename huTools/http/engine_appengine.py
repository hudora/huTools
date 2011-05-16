#!/usr/bin/env python
# encoding: utf-8
"""
engine_appengine.py implements urlfetch based queries for huTools.http.

See http://code.google.com/appengine/docs/python/urlfetch/overview.html for the basics of the
AppEngine capabilities.

Created by Maximillian Dornseif on 2010-10-24.
Copyright (c) 2010 HUDORA. All rights reserved.
"""


from google.appengine.api import apiproxy_stub_map, urlfetch, urlfetch_errors
from huTools.http import exceptions
import logging


def request(url, method, content, headers, timeout=25):
    """Does a HTTP Request via Google Appengine urlfetch Service.

    Incereases the default appengine timeout from 5 seconds to 25.
    (For Web-Requests this is reduced to 10s by the GAE Infrastructure)"""

    def urlfetch_timeout_hook(service, call, request, response):
        """Handler for setting timeout in urlfetch service

        See https://groups.google.com/group/google-appengine-python/browse_thread/thread/b5fcaa471f434bc6
        """

        if call != 'Fetch':
            return
        if not request.has_deadline():
            request.set_deadline(timeout)

    hooks = apiproxy_stub_map.apiproxy.GetPreCallHooks()
    hooks.Append('urlfetch_timeout_hook', urlfetch_timeout_hook, 'urlfetch')

    # on appengine debuging is always post mortem, so better log what we arde doing
    logging.debug('fetching %s %s', method, url)
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
