#!/usr/bin/env python
# encoding: utf-8
"""
printing.py simple minded toolkit for printing on CUPS.

Created by Maximillian Dornseif on 2006-11-19. BSD Licensed.
"""

import os
import os.path
import subprocess


__revision__ = "$Revision$"


def print_file(filename, jobname=None, printer=None, copies=1):
    """Print a file."""

    if not os.path.exists(filename):
        return

    args = ['/usr/local/bin/lpr', '-#%d' % copies]
    if printer:
        args.append('-P%s' % str(printer))
    args.append('"%s"' % filename)
    subprocess.call(args)


def print_data(data, jobname=None, printer=None, copies=1, printserver='printserver.local.hudora.biz'):
    """Print a datastream."""
    args = ['/usr/local/bin/lpr', '-#%d' % copies]
    if printer:
        args.append('-P%s' % str(printer))

    #if printserver:
    #    args.append('-H %s' % printserver)
    if jobname:
        args.append('-J %s  ' % jobname.replace("'\";./ ", "_"))

    pipe = subprocess.Popen(args, shell=False, stdin=subprocess.PIPE).stdin
    pipe.write(data)
    pipe.close()
