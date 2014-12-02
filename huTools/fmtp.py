#!/usr/bin/env python
# encoding: utf-8
"""
fmtp.py - huTools FMTP client

Created by Christian Klein on 2010-12-28.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

from __future__ import with_statement
import huTools.http
import huTools.hujson2 as json
import mimetypes
import os
import urlparse
import xml.etree.ElementTree as ET


class FMTPError(Exception):
    """FMTP-Exception"""
    def __init__(self, code, msg):
        super(FMTPError, self).__init__('%d %s' % (code, msg))
        self.code = code


def build_url(endpoint, queuename, guid=None):
    """Build url from endpoint and queuename, add document guid if necessary

    >>> build_url('http://example.com', 'q')
    'http://example.com/q/'
    >>> build_url('http://example.com', 'q', '45054')
    'http://example.com/q/45054/'
    """

    url = urlparse.urljoin(endpoint, queuename + '/')
    if guid:
        url = urlparse.urljoin(url, guid + '/')
    return url


def parse_xml(content):
    """Parse XML response

    >>> parse_xml('<data><messages><message><url>http://example.com/q/450/</url></message></messages></data>')
    ['http://example.com/q/450/']
    """

    tree = ET.fromstring(content)
    return [msg.findtext('url') for msg in tree.findall('messages/message')]


def parse_json(content):
    """Parse JSON response

    >>> parse_json('{"messages": [{"url": "http://example.com/q/45054/"}]}')
    [u'http://example.com/q/45054/']
    """

    result = json.loads(content)
    return [msg.get('url') for msg in result.get('messages', [])]


def get_list(endpoint, queuename, credentials=None):
    """Get list of messages"""

    content_type, parser = 'application/json', parse_json

    url = build_url(endpoint, queuename)
    headers = {'Accept': content_type}
    status, headers, content = huTools.http.fetch(url, method='GET', headers=headers, credentials=credentials)
    if status != 200:
        raise FMTPError(status, content)
    return parser(content)


def push(endpoint, queuename, guid, document, content_type='application/octet-stream', credentials=None):
    """Publish a message to a queue"""

    url = build_url(endpoint, queuename, guid)
    headers = {'Content-Type': content_type}
    status, headers, content = huTools.http.fetch(url,
                                                  method='POST',
                                                  content=document,
                                                  headers=headers,
                                                  credentials=credentials)
    if status != 201:
        raise FMTPError(status, content)


def pull(url, credentials=None):
    """Read a single message"""

    status, headers, content = huTools.http.fetch(url, method='GET', credentials=credentials)
    if status != 200:
        raise FMTPError(status, content)
    return content


def acknowledge(endpoint, queuename, guid, credentials=None):
    """Send acknowledgement for a message"""

    url = build_url(endpoint, queuename, guid)
    status, headers, content = huTools.http.fetch(url, method='DELETE', credentials=credentials)

    if status != 204:
        raise FMTPError(status, content)


def store(directory, filename, content):
    """Store document at path"""

    path = os.path.join(directory, filename)
    with open(path, 'w') as output:
        output.write(content)


def fetch(endpoint, queuename, directory='.', credentials=None):
    """Fetch all messages from a queue and store them in a directory"""

    if credentials is None:
        credentials = os.getenv('FMTP_CREDENTIALS', '')

    while True:
        messages = get_list(endpoint, queuename, credentials=credentials)
        if not messages:
            break

        url = messages[0]
        guid = url.replace('/', '\n').split()[-1]
        store(directory, guid, pull(url, credentials=credentials))
        acknowledge(endpoint, queuename, guid, credentials=credentials)


def send(endpoint, queuename, directory='.', delete=False, credentials=None):
    """Send all files from a directory"""

    if credentials is None:
        credentials = os.getenv('FMTP_CREDENTIALS', '')

    for fname in os.listdir(directory):
        path = os.path.join(directory, fname)
        data = open(path).read()

        mimetype, _ = mimetypes.guess_type(fname)
        if mimetype is None:
            mimetype = 'application/octet-stream'

        push(endpoint, queuename, fname, data, content_type=mimetype, credentials=credentials)
        if delete:
            os.unlink(path)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
