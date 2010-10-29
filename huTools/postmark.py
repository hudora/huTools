#!/usr/bin/env python
# encoding: utf-8
"""
postmark.py - support for the postmark mail sending API

Based on pytohn-postmark (C) 2009-2010 David Martorana, Wildbit LLC, Python Software Foundation.

Created by Maximillian Dornseif on 2010-09-27.
Copyright (c) 2010 HUDORA. All rights reserved.
"""


import hujson
import logging
import urllib2


__POSTMARK_URL__ = 'http://api.postmarkapp.com/'


def send_mail(message, api_key=None):
        '''
        Send the email through the Postmark system.

        message is a dict containing:
        Sender:         Who the email is coming from, in either
                        "name@email.com" or "First Last <name@email.com>" format
        To:             Who to send the email to, in either
                        "name@email.com" or "First Last <name@email.com>" format
                        Can be multiple values separated by commas (limit 20)
        Subject:        Subject of the email

        optional elements:
        TextBody:       Email message in plain text
        HtmlBody:       Email message in HTML
        Cc:             Who to copy the email to, in either
                        "name@email.com" or "First Last <name@email.com>" format
                        Can be multiple values separated by commas (limit 20)
        Bcc:            Who to blind copy the email to, in either
                        "name@email.com" or "First Last <name@email.com>" format
                        Can be multiple values separated by commas (limit 20)
        Tag:            Use for adding categorizations to your email
        Attachments:    A list of attachments. Attachments can be either
                        a list of {name, data, content_type} dicts,
        '''

        if 'Sender' in message and ('From' not in message):
            message['From'] = message['Sender']
        for attr in 'From To Subject'.split():
            if attr not in message:
                raise RuntimeError('missing Parameter %s' % attr)
        if ('TextBody' not in message) and ('HtmlBody' not in message):
            raise RuntimeError('missing Body %r' % message)

        attachments = []
        for attachment in message.get('Attachments', []):
            attachments.append({
                    "Name": attachment['Name'],
                    "Content": attachment['Content'].encode('base64'),
                    "ContentType": attachment['ContentType'],
                    })
        if attachments:
            message['Attachments'] = attachments

        # Set up the url Request
        req = urllib2.Request(
            __POSTMARK_URL__ + 'email',
            hujson.dumps(message),
            {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-Postmark-Server-Token': api_key,
            }
        )

        logging.debug('Accessing %semail' % __POSTMARK_URL__)
        try:
            result = urllib2.urlopen(req)
            result.close()
            if result.code == 200:
                return True
            else:
                raise RuntimeError('Postmark Return code %d: %s' % (result.code, result.msg))
        except urllib2.HTTPError, err:
            if err.code == 401:
                raise RuntimeError('Sending Unauthorized - incorrect API key.', err)
            elif err.code == 422:
                try:
                    jsontxt = err.read()
                    jsonobj = hujson.loads(jsontxt)
                    desc = jsonobj['Message']
                except:
                    desc = 'Description not given'
                raise RuntimeError('Unprocessable Entity: %s' % desc)
            elif err.code == 500:
                raise RuntimeError('Internal server error at Postmark. Admins have been alerted.', err)
        except urllib2.URLError, err:
            if hasattr(err, 'reason'):
                raise RuntimeError("URLError: Failed to reach the server: %s (See 'inner_exception' for details)" % err.reason, err)
            elif hasattr(err, 'code'):
                raise RuntimeError("URLError: %d: The server couldn't fufill the request. (See 'inner_exception' for details)" % err.code, err)
            else:
                raise RuntimeError("URLError: The server couldn't fufill the request. (See 'inner_exception' for details)", err)
