#!/usr/bin/env python
# encoding: utf-8
"""
xml.py

Created by Christian Klein on 2010-02-26.
Copyright (c) 2010 HUDORA GmbH. All rights reserved.
"""

import couchdb.client

def setup_couchdb(servername, database):
    """Get a connection handler to the CouchDB Database, creating it when needed."""

    server = couchdb.client.Server(servername)
    if database in server:
        return server[database]
    else:
        return server.create(database)
