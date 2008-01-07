#!/usr/bin/env python
# encoding: utf-8
"""
printing.py simple minded toolkit for printing on CUPS.

Created by Maximillian Dornseif on 2006-11-19. BSD Licensed.
"""

import os

__revision__ = "$Revision$"

def print_file(filename, jobname=None, printer=None, copies=1):
    """Print a file."""
    args = [] # '-n %d' % copies]
    if printer:
        args.append('-P %r' % str(printer))
    for c in range(copies):
        os.system('/usr/local/bin/lpr %s %r' % (' '.join(args), filename))

def print_data(data, jobname=None, printer=None, copies=1, printserver='printserver.local.hudora.biz'):
    """Print a file."""
    args = [] # ['-n %d' % copies]
    if printer:
        args.append('-P %r' % str(printer))
    #if printserver:
    #    args.append('-H %r' % str(printserver))
    #if jobname:
    #    args.append('-J %r' % jobname.replace("'\";./ ", "_"))
    os.system('echo /usr/local/bin/lpr %s >> /tmp/huTools_lplog' % (' '.join(args),))
    for c in range(copies):
        fd = os.popen('/usr/local/bin/lpr %s >> /tmp/huTools_lplog' % (' '.join(args),), 'w')
        fd.write(data)
        fd.close()
