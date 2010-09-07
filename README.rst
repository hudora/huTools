=======
huTools
=======

huTools is a small collection of helpful tools we use.

 * calendar - date based calculations and format conversions: `calendar.formats <http://github.com/hudora/huTools/blob/master/huTools/calendar/formats.py>`_, `calendar.workdays <http://github.com/hudora/huTools/blob/master/huTools/calendar/workdays.py>`_
 * `checksummming <http://github.com/hudora/huTools/blob/master/huTools/checksumming.py>`_ - calculate various checksums
 * `couch <http://github.com/hudora/huTools/blob/master/huTools/couch.py>`_ - CouchDB helper functions
 * `decorators <http://github.com/hudora/huTools/blob/master/huTools/decorators.py>`_ - various helpful decorators
 * `huLint <http://github.com/hudora/huTools/blob/master/huTools/huLint.py>`_ - Code Quality Checking
 * `luids <http://github.com/hudora/huTools/blob/master/huTools/luids.py>`_ - locally unique user-ids
 * `NetStringIO <http://github.com/hudora/huTools/blob/master/huTools/NetStringIO.py>`_
 * `obfuscation <http://github.com/hudora/huTools/blob/master/huTools/obfuscation.py>`_ - String Obfuscation
 * `printing <http://github.com/hudora/huTools/blob/master/huTools/printing.py>`_ - access printers
 * `ReReadingConfigParser <http://github.com/hudora/huTools/blob/master/huTools/ReReadingConfigParser.py>`_ - ConfigParser which detects changes in config files
 * `robusttypecasts <http://github.com/hudora/huTools/blob/master/huTools/robusttypecasts.py>`_ - type conversionts that seldom fail
 * structured - access dicts like an object and the other way arround
 * `unicode <http://github.com/hudora/huTools/blob/master/huTools/unicode.py>`_ - real-world unicode handling
 * `world <http://github.com/hudora/huTools/blob/master/huTools/world.py>`_ - country codes
 * `xmltools <http://github.com/hudora/huTools/blob/master/huTools/xmltools.py>`_ - various XML helpers


It also installs the famous reindent.py code quality checker. Try 
`reindent.py .` to fix your current source tree.


Installation
------------

The easiest way to get huTools is if you have setuptools_ installed::

	easy_install huTools

Without setuptools, it's still pretty easy. Download the huTools.tgz file from 
`huTools's Cheeseshop page`_, untar it and run::

	python setup.py install

.. _huTools's Cheeseshop page: http://pypi.python.org/pypi/huTools/
.. _setuptools: http://peak.telecommunity.com/DevCenter/EasyInstall


Help and development
====================

If you'd like to help out, you can fork the project
at http://github.com/hudora/huTools and report any bugs 
at http://github.com/hudora/huTools/issues.

See `CHANGES <http://github.com/hudora/huTools/blob/master/CHANGES>`_
for version differences.
