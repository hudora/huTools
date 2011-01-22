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

"""

# Created by Maximillian Dornseif on 2010-10-24.
# Copyright (c) 2010 HUDORA. All rights reserved.

from huTools.http import tools
import cgi
import poster_encode
import urlparse

try:
    import engine_httplib2
    request = engine_httplib2.request
except ImportError:
    import engine_appengine
    request = engine_appengine.request


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

    myheaders = {'Accept-Encoding': 'gzip;q=1.0, *;q=0',
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
        authheader = "Basic %s" % credentials.encode('base64').strip()
        myheaders["Authorization"] = authheader

    return request(url, method, content, myheaders, timeout)
