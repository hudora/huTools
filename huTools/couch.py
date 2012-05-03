#!/usr/bin/env python
# encoding: utf-8
"""
couch.py

Created by Christian Klein on 2010-02-26.
Copyright (c) 2010 HUDORA GmbH. All rights reserved.
"""

import couchdb.client
import warnings

def setup_couchdb(servername, database):
    """Get a connection handler to the CouchDB Database, creating it when needed."""

    warnings.warn("hutools.couch is deprecated", DeprecationWarning, stacklevel=2)
    server = couchdb.client.Server(servername)
    if database in server:
        return server[database]
    else:
        return server.create(database)
