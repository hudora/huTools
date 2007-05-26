#!/usr/bin/env python
# encoding: utf-8
"""
printing.py simple minded toolkit for printing on CUPS.

Created by Maximillian Dornseif on 2006-11-19.
"""

import os

def print_file(filename, jobname=None, printer=None, copies=1):
    """Print a file."""
    args = [] # '-n %d' % copies]
    if printer:
        args.append('-P %r' % str(printer))
    for c in range(copies):
        os.system('/usr/local/bin/lpr %s %r' % (' '.join(args), filename))
    os.system('echo "/usr/local/bin/lpr %s %r" > /tmp/foo' % (' '.join(args), filename))
    if jobname:
        args.append('-J %r' % jobname.replace("'", ""))
    os.system('echo "/usr/local/bin/lpr %s %r" >> /tmp/foo' % (' '.join(args), filename))
