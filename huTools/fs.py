#!/usr/bin/env python
# encoding: utf-8
"""
fs.py filesystem-related functions

Created by Maximillian Dornseif on 2008-08-16.
Copyright (c) 2008 HUDORA. Consider it BSD Licensed.
"""

import os


def makedirhier(dirnmame):
    """Created 'dirname' if needes and all intermediate directories."""

    if not os.path.exists(dirnmame):
        os.makedirs(dirnmame)
