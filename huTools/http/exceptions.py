#!/usr/bin/env python
# encoding: utf-8
"""
exceptions.py

Created by Christian Klein on 2011-05-16.
Copyright (c) 2011 HUDORA GmbH. All rights reserved.
"""


class WrongStatusCode(RuntimeError):
    """Thrown if the Server returns a unexpected status code."""
    pass


class Timeout(RuntimeError):
    """Thrown on request timeout"""
    pass
