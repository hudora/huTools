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

# Created by Maximillian Dornseif on 2010-10-24.
# Copyright (c) 2010, 2011 HUDORA. All rights reserved.

from huTools import hujson
from huTools.http import exceptions
from huTools.http import tools
import cgi
import poster_encode
import urllib
import urlparse


# This is somewhat clumsy to make static code checkers happy
request = None
try:
    import engine_appengine
    request = engine_appengine.request
except ImportError:
    import engine_httplib2
    request = engine_httplib2.request


def prepare_headers(url, content='', method='GET', credentials=None, headers=None, multipart=False, ua='',
                    timeout=25):
    """Prepares a request, returns (url, method, content, headers, timeout)"""

    myheaders = {'Accept-Encoding': 'gzip',
                 'User-Agent': '%s/huTools.http (gzip)' % ua}
    if headers:
        myheaders.update(headers)
    if method == 'POST':
        if hasattr(content, 'items'):
            # we assume content is a dict which needs to be encoded
            # decide to use multipart/form-data encoding or application/x-www-form-urlencoded
            for val in content.values():
                if hasattr(val, 'read'):  # file() or StringIO()
                    multipart = True
            if multipart:
                datagen, mp_headers = poster_encode.multipart_encode(content)
                myheaders.update(mp_headers)
                content = "".join(datagen)
            else:
                myheaders.update({'Content-Type': 'application/x-www-form-urlencoded'})
                content = tools.urlencode(content)
    else:
        # url parmater encoding
        if hasattr(content, 'items'):
            scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
            qdict = cgi.parse_qs(query)
            # ugly Unicode issues, see http://bugs.python.org/issue1712522
            qdict.update(content)
            query = tools.urlencode(qdict)
            url = urlparse.urlunparse((scheme, netloc, path, params, query, fragment))
            content = ''
    # convert all header values to strings (what about unicode?)
    for key, val in myheaders.items():
        myheaders[key] = str(val)
    # add authentication
    if credentials and not 'Authorization' in myheaders.keys():
        # ''.encode('b64') zerbricht lange Strings (also bei langen Credentials)
        # in mehrere Zeilen, was einer Verwendung als Wert im HTTP-Header extrem
        # abtraeglich ist. Aufgetaucht ist das Problem bei den Login-Daten fuer
        # den Import der Shopify-Auftraege aus dem hySkate-Shop. Zur Loesung werden
        # deshalb alle moeglichen Einzelzeilen wieder zu einer Zeile zusammengezogen.
        authheader = 'Basic %s' % ''.join(credentials.encode('base64').strip().split())
        myheaders["Authorization"] = authheader
    return url, method, content, myheaders, timeout


def fetch(url, content='', method='GET', credentials=None, headers=None, multipart=False, ua='', timeout=25):
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

    return request(*prepare_headers(url, content, method, credentials, headers, multipart, ua, timeout))


def fetch2xx(url, content='', method='GET', credentials=None, headers=None, multipart=False, ua='',
             timeout=25):
    """Like `fetch()` but throws a RuntimeError if the status code is < 200 or >= 300."""
    status, rheaders, rcontent = fetch(url, content, method, credentials, headers, multipart, ua, timeout)
    if (status < 200) or (status >= 300):
        raise exceptions.WrongStatusCode(u"%s: Fehler: %r" % (status, rcontent))
    return status, rheaders, rcontent


def fetch_json2xx(url, content='', method='GET', credentials=None, headers=None, multipart=False, ua='',
             timeout=25):
    """Like `fetch2xx()` but JSON-decodes the returned content and returns only that."""
    status, rheaders, rcontent = fetch2xx(url, content, method, credentials, headers, multipart, ua, timeout)
    if not rheaders.get('content-type', '').startswith('application/json'):
        raise TypeError(u"Ungueltiger Content-Type %r: %r" % (rheaders.get('content-type', ''), rcontent))
    return hujson.loads(rcontent)


def add_query(url, params):
    """
    Add GET parameters to a given URL

    >>> add_query('/sicrit/', {'passphrase': 'fiftyseveneleven'})
    '/sicrit/?passphrase=fiftyseveneleven'
    >>> add_query('/sicrit/test.html?hello=world', {'passphrase': 'fiftyseveneleven'})
    '/sicrit/test.html?hello=world&passphrase=fiftyseveneleven'
    """

    url_parts = list(urlparse.urlparse(url))
    query = dict(cgi.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)
