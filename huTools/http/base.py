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

Created by Maximillian Dornseif on 2010-10-24.
Copyright (c) 2010, 2011 HUDORA. All rights reserved.
"""
import cgi
import logging

from huTools import hujson2
from huTools.http import exceptions
from huTools.http import tools


# This is somewhat clumsy to make static code checkers happy
request = None
engine = None
try:
    import engine_appengine
    request = engine_appengine.request
    AsyncHttpResult = engine_appengine.AsyncHttpResult
except ImportError:
    import engine_httplib2
    request = engine_httplib2.request
    AsyncHttpResult = engine_httplib2.AsyncHttpResult


def fetch(url, content='', method='GET', credentials=None, headers=None, multipart=False, ua='', timeout=50,
          caching=None):
    """Does a HTTP request with method `method` to `url`.

    Returns (status, headers, content) whereas `status` is an integer status code, `headers` is a dict
    containing the headers sent by the server and `content` is the body of the http response.

    Parameters to fetch are::

    * `url` is the fully qualified request URL. It may contain query prameters.
    * `content` is the request body to be sent. It may be a dict which for all requests expect POST
      is converted to query parameters. If there are query parameters already in the `url` they are merged
      with `content`. For POST requests the data is encoded as application/x-www-form-urlencoded
      or multipart/form-data and encoded. If the parameter `multipart` is `True` or if one of the values
      in content has a `name` attribute (which is the case for file objects) multipart encoding is choosen.
    * `headers` is a dict of header values
    * `credentials` can be a user:password combination
    * `ua` should be an additional User Agent string
    * `timeout` is the maximum number of seconds the request might take. This is advisory and may not be
       enforced.
    """
    return request(*tools.prepare_headers(url, content, method, credentials, headers, multipart, ua,
                                          timeout, caching))


def fetch2xx(url, content='', method='GET', credentials=None, headers=None, multipart=False, ua='',
             timeout=50, caching=None):
    """Like `fetch()` but throws a RuntimeError if the status code is < 200 or >= 300."""
    status, rheaders, rcontent = fetch(url, content, method, credentials, headers, multipart, ua, timeout,
                                       caching)
    if (status < 200) or (status >= 300):
        raise exceptions.WrongStatusCode(u"%s: Fehler: %r" % (status, rcontent))
    return status, rheaders, rcontent


def fetch_json2xx(url, content='', method='GET', credentials=None, headers=None, multipart=False, ua='',
             timeout=50, caching=None):
    """Like `fetch2xx()` but JSON-decodes the returned content and returns only that."""
    status, rheaders, rcontent = fetch2xx(url, content, method, credentials, headers, multipart, ua, timeout,
                                          caching)
    if not rheaders.get('content-type', '').startswith('application/json'):
        raise TypeError(u"Ungueltiger Content-Type %r: %r" % (rheaders.get('content-type', ''), rcontent))
    return hujson2.loads(rcontent)


def fetch_async(url, content='', method='GET', credentials=None, headers=None, multipart=False, ua='',
                timeout=50, returnhandler=lambda x, y, z: (x, y, z), caching=None):
    """Initiate a asyncrounus HTTP Request and return a result object.

    `fetch_async(...).get_result()` can be used to emulate `fetch(...)`.
    You can use `returnhandler` to postprocess the returned http data. Typical use in a library:

        def get_eap_async(artnr):
            def returnhandler(status, headers, content):
                if status == 200:
                    return json.loads(content)
                else:
                    raise RuntimeError("%d: %s" % (status, content))

            return fetch_async('http://example.com/foo', returnhandler=returnhandler)

    Callers could now use
        >>> get_eap_async(artnr).get_result()
    """
    o = AsyncHttpResult(caching)
    o.fetch(url, content, method, credentials, headers, multipart, ua, timeout, returnhandler)
    return o


def fetch_json2xx_async(url, content='', method='GET', credentials=None, headers=None, multipart=False,
             ua='', timeout=50, returnhandler=lambda x: x, caching=None):
    """Like `fetch_async()` but returnhandler is called with decoded jsondata."""
    def decodingreturnhandler(status, rheaders, rcontent):
        """Closure to do the json decoding and then call the provided returnhandler"""
        if (status < 200) or (status >= 300):
            raise exceptions.WrongStatusCode(u"%s: Fehler: %r" % (status, rcontent))
        # Warnig! httplib2 ist case sensitive for header field names.
        if not rheaders.get('Content-Type', '').startswith('application/json'):
            logging.debug("no valid content type: %r", rheaders)
            # There seems to be an interesting issue with the AppEngine Frontend Cache Servers:
            # When serving from the cache to an AppEngine client (date being rquested from an other
            # AppEngine Application) the content type header seems to get dropped completely.
            # So wo only check for a missmatched header but ignore empty ones.
            # So far this has been only observed with async requests.
            if rheaders.get('Content-Type', None) is not None:
                raise TypeError(u"%s: Ungueltiger Content-Type %r: %r" % (url,
                                    rheaders.get('Content-Type', ''), rcontent))
        return returnhandler(hujson2.loads(rcontent))

    return fetch_async(url, content, method, credentials, headers, multipart, ua, timeout,
                       decodingreturnhandler, caching)


def add_query(url, params):
    """Add a Query string to an url. Obsolete."""
    import warnings
    import huTools.http.tools
    warnings.warn("huTools.http.add_query() is obsolete, use huTools.http.tools.add_query() instead",
                  DeprecationWarning, stacklevel=2)
    return huTools.http.tools.add_query(url, params)


def json_iterator(url, method='GET', content=None, credentials=None, datanodename='data'):
    """
    Rufe JSON-Daten ab.
 
    Es wird die seitenweise Darstellung von gaetk.BasicHandler.paginate unterstützt.
    """

    while True:
        try:
            response = fetch_json2xx(url,
                                     method=method,
                                     content=content,
                                     credentials=credentials)
        except exceptions.WrongStatusCode:
            break
 
        for element in response[datanodename]:
            yield element
 
        if not response['more_objects']:
            break
        else:
            cursor_information = response.get('next_qs', '')
            tmp = cgi.parse_qs(cursor_information)
            for key, values in tmp.items():
                content[key] = values[0]
