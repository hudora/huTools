#!/usr/bin/env python
# encoding: utf-8
"""
engine_httplib2.py implements httplib2 based queries for huTools.http

Created by Maximillian Dornseif on 2010-10-24.
Copyright (c) 2010 HUDORA. All rights reserved.
"""


_http = None


def request(url, method, content, headers, timeout=15):
    """Does a HTTP Request via httplib2 Service."""

    global _http
    if not _http:
        import huTools.http._httplib2
        _http = huTools.http._httplib2.Http()
    
    headers['User-Agent'] = headers.get('User-Agent', '') + ' (httplib2)'
    resp, content = _http.request(url, method, content, headers=headers)
    replyheaders = {}
    replyheaders.update(resp)
    return int(resp.status), replyheaders, content
