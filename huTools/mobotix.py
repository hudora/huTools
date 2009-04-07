#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Get picture data from a mobotix cam.
    
Created by Jens Diemer on 2009-03-13.
Copyright (c) 2009 HUDORA. All rights reserved.
"""

import urllib2
import unittest


def get_mobotix_pic(url, content_type='image/jpeg'):
    """
    Shortcut function for getting the content of a mobotix picture directly.
    If something happend, a MobotixError would be raised. So you must only catch this.
    """
    try:
        handle = urllib2.urlopen(url)
    except Exception, err:
        raise MobotixError("Can't get mobotix pic from %r: %s" % (url, err))
    
    if handle.code != 200:
        raise MobotixError("return code != 200, it was: %s" % handle.code)
    
    is_content_type = handle.headers.get('content-type')
    if is_content_type != content_type:
        raise MobotixError("content-type != %s, it's: %s" % (content_type, is_content_type))

    imagedata = handle.read()
    handle.close()
    
    return imagedata



class MobotixError(Exception):
    """ error getting the mobotix screenshot """
    pass


class _MobotixTests(unittest.TestCase):
    """
    simple unittest for get_mobotix_pic()
    This unitest only works, if the used urls works as well as thought :)
    """
    GIF_URL = 'http://s.hdimg.net/layout06/hudora.gif'
    
    def test_get_gif_file(self):
        content = get_mobotix_pic(url=self.GIF_URL, content_type='image/gif')
        self.failUnless(content.startswith("GIF89a"))
        
    def test_wrong_content_type(self):
        self.failUnlessRaises(MobotixError, get_mobotix_pic, url=self.GIF_URL, content_type='image/jpeg')

    def test_wrong_domain(self):
        self.failUnlessRaises(MobotixError, get_mobotix_pic, url="http://www.a_wrong_url.tld")
        
    def test_wrong_path(self):
        self.failUnlessRaises(MobotixError, get_mobotix_pic, url="http://www.hudora.de/gibtesnicht.jpeg")


if __name__ == '__main__':
    unittest.main()
