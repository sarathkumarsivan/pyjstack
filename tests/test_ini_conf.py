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
import os
from pyjstack.configurer import read_ini_conf


class TestINIConfMethods(unittest.TestCase):

    def test_init_conf_exists(self):
        self.assertEquals(os.path.exists('conf/pyjstack.ini'), True)

    def test_read_ini_conf(self):
        conf = read_ini_conf('conf/pyjstack.ini')
        print conf
        print conf['email']['email']
        self.assertEqual(conf.get('email', 'email'), 'user@gmail.com')
        self.assertEqual(conf.get('email', 'from_email'), 'user@pyjstack.com')
        self.assertEqual(conf.get('email', 'smptp_server'), 'smtp.cloud.com')
        self.assertEqual(conf.get('email', 'smtp_port'), '25')
        self.assertEqual(conf.get('email', 'attachment'), '/tmp/pyjstack/attachment.tar.gz')
        self.assertEqual(conf.get('email', 'password'), 'secret')
        self.assertEqual(conf.get('email', 'subject'), 'Email Notification')
        self.assertEqual(conf.get('email', 'to_email')[0], 'user1@gmail.com')
        self.assertEqual(conf.get('email', 'to_email')[1], 'user2@gmail.com')
        self.assertEqual(conf.get('jstack','pid'), '10023')
        self.assertEqual(conf.get('jstack','count'), '12')
        self.assertEqual(conf.get('jstack','delay'), '2')


if __name__ == '__main__':
    unittest.main()
