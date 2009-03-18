#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    mobotix
    ~~~~~~~
    
    Get picture data from a mobotix cam.
    
    FIXME: this file should moved.
    
    Created by Jens Diemer on 2009-03-13.
    Copyright (c) 2009 HUDORA. All rights reserved.
"""
import urllib2



class Mobotix(object):
    """
    for a Django Storage save method.
    """
    def __init__(self, url, content_type='image/jpeg'):
        self.url = url
        self.content_type = content_type
        self.handle = None
        
    def open(self):
        try:
            self.handle = urllib2.urlopen(self.url)
        except Exception, err:
            raise MobotixError("Can't get mobotix pic: %s" % err)
        
        if self.handle.code != 200:
            raise MobotixError("return code != 200, it was: %s" % f.code)
        
        is_content_type = self.handle.headers.get('content-type')
        if is_content_type != self.content_type:
            raise MobotixError("content-type != %s, it's: %s" % (self.content_type, is_content_type))
        
    def read(self):
        imagedata = self.handle.read()
        self.handle.close()
        self.handle = None
        return imagedata


def get_mobotix_pic(url, content_type='image/jpeg'):
    """
    shortcut function for getting the content of a mobotix picture directly.
    """
    m = Mobotix(url)
    m.open()
    imagedata = m.read()
    return imagedata



class MobotixError(Exception):
    """ error getting the mobotix screenshot """
    pass




if __name__ == '__main__':
    m = Mobotix(url='http://mobotix02.local.hudora.biz/record/current.jpg')
    print "open:", m.url
    m.open()
    print "Response code:", m.handle.code
    print "content: %r..." % m.read()[:15]