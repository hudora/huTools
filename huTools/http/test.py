#!/usr/bin/env python
# encoding: utf-8
"""
test.py

Created by Maximillian Dornseif on 2010-10-24.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import unittest
from huTools.http import fetch


class testTests(unittest.TestCase):

    def test_fetch_get_basic(self):
        status, header, body = fetch('http://www.google.com')
        assert status == 200
        status, header, body = fetch('http://www.postbin.org/186ndf2', {'q': 'hudora'})
        assert status == 200
        status, header, body = fetch('http://www.postbin.org/186ndf2', {'keyg': 'value', 'just a test': 212})
        assert status == 200

    def test_fetch_get_unicode(self):
        status, header, body = fetch('http://www.postbin.org/186ndf2',
                                     {'kühg1': 'Iñtërnâtiônàlizætiøn'})
        assert status == 200
        status, header, body = fetch('http://www.postbin.org/186ndf2',
                                     {'kühg2': u'Iñtërnâtiônàlizætiøn'})
        assert status == 200
        status, header, body = fetch('http://www.postbin.org/186ndf2',
                                     {u'kühg3': 'Iñtërnâtiônàlizætiøn'})
        assert status == 200

    def test_fetch_post_basic(self):
        status, header, body = fetch('http://www.postbin.org/186ndf2',
        {'keyp1': 'value', 'just a test': 212}, 'POST')
        assert status == 201

    def test_fetch_post_file(self):
        status, header, body = fetch('http://www.postbin.org/186ndf2',
                                     {'hosts': open('/etc/hosts', 'r')}, 'POST')
        status, header, body = fetch('http://www.postbin.org/186ndf2',
                                     {'hosts': open('/etc/hosts', 'r'), 
                                      'unicode': u'Iñtërnâtiônàlizætiøn'}, 'POST')
        assert status == 201

    def test_fetch_post_unicode(self):
        status, header, body = fetch('http://www.postbin.org/186ndf2',
                                     {'kuehp1': 'Iñtërnâtiônàlizætiøn'}, 'POST')
        assert status == 201
        status, header, body = fetch('http://www.postbin.org/186ndf2',
                                     {'kühp2': 'Iñtërnâtiônàlizætiøn'}, 'POST')
        assert status == 201
        status, header, body = fetch('http://www.postbin.org/186ndf2',
                                     {'kühp3': u'Iñtërnâtiônàlizætiøn'}, 'POST')
        assert status == 201
        status, header, body = fetch('http://www.postbin.org/186ndf2',
                                     {u'kühp4': u'Iñtërnâtiônàlizætiøn'}, 'POST')
        assert status == 201


if __name__ == '__main__':
    unittest.main()
