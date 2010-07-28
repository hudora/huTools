#!/usr/bin/env python
# encoding: utf-8
"""
Client library for REST APIs

Created by Christian Klein on 2010-07-21.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import httplib2
import os
import tempfile
import urllib
import urlparse
import simplejson as json


def build_url(base, *args):
    """
    Create URLs for a REST API
    
    >>> build_url('orders_', 1)
    'orders/1/'
    >>> build_url('cool_mc_cool_', 1, 2)
    'cool/1/mc/2/cool/'
    >>> build_url('cool_mc_cool_', 1, 2, 3)
    'cool/1/mc/2/cool/3/'
    """
    
    tmp = []
    args = list(args)
    components = base.split('_')
    
    while components:
        tmp.append(components.pop(0))
        if args:
            tmp.append(str(args.pop(0)))
    return os.path.join(*tmp)


class ApiException(Exception):
    """Basisklasse für Exceptions"""
    pass

class ApiNotFoundException(ApiException):
    pass

class ApiForbiddenException(ApiException):
    pass

class ApiUnauthorizedExecption(ApiException):
    pass

class ApiServerErrorExecption(ApiException):
    pass


class Client(object):
    """
    Client for RESTful API
    
    All data is encoded as JSON.
    """
    
    def __init__(self, username, password, endpoint):
        self.username = username
        self.password = password
        self.endpoint = endpoint
        
        cachedir = os.path.join(tempfile.gettempdir(), 'robotrock')
        self.connection = httplib2.Http(cache=cachedir, timeout=20)
        self.connection.add_credentials(username, password, domain=urlparse.urlsplit(self.endpoint).netloc)
    
    def __getattr__(self, method):
        def handler(*args, **kwargs):
            """doc for handler"""
            return self(method, *args, **kwargs)
        return handler

    def __call__(self, fnc, *args, **kwargs):
        """Do a remote procedure call via HTTP"""
        
        headers = {'content-type':'application/json'}            
        path = os.path.join(self.endpoint, build_url(fnc, *args), '')
        
        if 'params' in kwargs:
            path = "%s?%s" % (path, urllib.urlencode(kwargs.pop('params')))

        if kwargs:
            body = json.dumps(kwargs)
            method = 'POST'
        else:
            body = None
            method = 'GET'
        
        response, content = self.connection.request(path, method=method, body=body, headers=headers)
        
        #if response.status == 200:
        #    print "OK"
        if response.status == 201: 
            return { 'status': 201,
                     'success': 'created' }
        if response.status == 401:
            raise ApiUnauthorizedExecption()
        elif response.status == 403:
            raise ApiForbiddenException()
        elif response.status == 404:
            raise ApiNotFoundException()
        elif response.status == 500:
            raise ApiServerErrorExecption()

        try:
            return json.loads(content)
        except:
            return {'status': response.status,
                    'error': 'unparseable response',
                    'data': content }

    
    def close(self):
        """
        Close API Client.
        
        Delete the connection(pool)
        """
        del(self.connection)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
