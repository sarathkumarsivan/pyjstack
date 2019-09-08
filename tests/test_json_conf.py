#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Sarath Kumar Sivan, https://github.com/sarathkumarsivan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import unittest
from pyjstack.sysconfig import read_json_conf

CONF_PATH = 'conf/pyjstack-conf.json'

class TestJSONConfMethods(unittest.TestCase):

    def test_read_json_conf(self):
        conf = read_json_conf(CONF_PATH)
        email = conf['email']
        self.assertEqual(email['from_email'], 'user@pyjstack.com')
        self.assertEqual(email['smptp_server'], 'smtp.cloud.com')
        self.assertEqual(email['smtp_port'], '25')
        self.assertEqual(email['attachment'], '/tmp/pyjstack/attachment.tar.gz')
        self.assertEqual(email['password'], 'secret')
        self.assertEqual(email['email'], 'user@gmail.com')
        self.assertEqual(email['subject'], 'Email Notification')
        to_email = email['to_email']
        self.assertEqual(to_email[0], 'user1@gmail.com')
        self.assertEqual(to_email[1], 'user2@gmail.com')
        jstack = conf['jstack']
        self.assertEqual(jstack['pid'], '10023')
        self.assertEqual(jstack['count'], '12')
        self.assertEqual(jstack['delay'], '2')


if __name__ == '__main__':
    unittest.main()
