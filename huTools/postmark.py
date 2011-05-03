#!/usr/bin/env python
# encoding: utf-8
"""
postmark.py - support for the postmark mail sending API

Based on pytohn-postmark (C) 2009-2010 David Martorana, Wildbit LLC, Python Software Foundation.

Created by Maximillian Dornseif on 2010-09-27.
Copyright (c) 2010 HUDORA. All rights reserved.
"""
import email.utils
import hujson
import logging
import unittest
import urllib2


__POSTMARK_URL__ = 'http://api.postmarkapp.com/'


def format_addr(address, encoding='utf-8'):
    """Format an email adress

    If the domainname contains non-ASCII characters an IDNA encoded address will be returned.
    """

    if isinstance(address, str):
        address = address.decode(encoding)

    realname, address = email.utils.parseaddr(address)
    localpart, domain = address.split('@', 1)
    address = u'@'.join((localpart, domain.encode('idna')))
    return email.utils.formataddr((realname, address))


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

        # Do IDNA encoding of domainnames if necessary
        message['From'] = format_addr(message['From'])
        message['To'] = format_addr(message['To'])
        if message.get('Cc'):
            message['Cc'] = ','.join([format_addr(address) for address in message['Cc'].split(',')])
        if message.get('Bcc'):
            message['Bcc'] = ','.join([format_addr(address) for address in message['Bcc'].split(',')])

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
                raise RuntimeError(("URLError: Failed to reach the server: %s (See 'inner_exception' for"
                                    " details)") % err.reason, err)
            elif hasattr(err, 'code'):
                raise RuntimeError(("URLError: %d: The server couldn't fufill the request. (See"
                                    " 'inner_exception' for details)") % err.code, err)
            else:
                raise RuntimeError("URLError: The server couldn't fufill the request. (See 'inner_exception'"
                                   " for details)", err)


class EncodingTest(unittest.TestCase):
    """Unittest for fomat_addr"""

    def test_simple(self):
        """Test simple address without realname"""
        self.assertEqual(format_addr('info@example.com'), u'info@example.com')

    def test_simple_unicode(self):
        """Test simple address without realname (given as unicode)"""
        self.assertEqual(format_addr(u'info@example.com'), u'info@example.com')

    def test_realname(self):
        """Test address with a realname"""
        self.assertEqual(format_addr('Info Board <info@example.com'), u'Info Board <info@example.com>')

    def test_realname_unicode(self):
        """Test address with a realname"""
        self.assertEqual(format_addr(u'Info Board <info@example.com'), u'Info Board <info@example.com>')

    def test_idna_simple(self):
        """Test simple address with non-ASCII characters without realname"""
        self.assertEqual(format_addr('info@smör.de'), u'info@xn--smr-tna.de')

    def test_idna_simple_unicode(self):
        """Test simple address with non-ASCII characters without realname (given as unicode)"""
        self.assertEqual(format_addr(u'info@smör.de'), u'info@xn--smr-tna.de')

    def test_idna_realname(self):
        """Test address with an non-ASCII characters and a realname"""
        self.assertEqual(format_addr('Info <info@smör.de>'), u'Info <info@xn--smr-tna.de>')

    def test_idna_realname_unicode(self):
        """Test address with an non-ASCII characters and a realname (given as unicode)"""
        self.assertEqual(format_addr(u'Info <info@smör.de>'), u'Info <info@xn--smr-tna.de>')

    def test_idna_realname2(self):
        """Test address with an non-ASCII characters and a realname"""
        self.assertEqual(format_addr('iñfø <info@smör.de>'), u'iñfø <info@xn--smr-tna.de>')

    def test_idna_realname2_unicode(self):
        """Test address with an non-ASCII characters and a realname (given as unicode)"""
        self.assertEqual(format_addr(u'iñfø <info@smör.de>'), u'iñfø <info@xn--smr-tna.de>')

    def test_idna_latin1(self):
        """Test IDNA encoding for latin1 encoded strings"""

        email_address = u'info@smör.de'.encode('latin1')
        self.assertEqual(format_addr(email_address, encoding='latin1'), u'info@xn--smr-tna.de')


if __name__ == "__main__":
    unittest.main()
