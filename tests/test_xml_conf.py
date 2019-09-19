import unittest

from pyjstack.sysconfig import read_xml_conf
from pyjstack import CONF_XML_PATH


class TestXMLConfMethods(unittest.TestCase):

    def test_read_json_conf(self):
        conf = read_xml_conf(CONF_XML_PATH)
        self.assertEqual(conf.email.email.contents[0], 'user@gmail.com')
        self.assertEqual(conf.email.password.contents[0], 'secret')
        self.assertEqual(conf.email.smptp_server.contents[0], 'smtp.cloud.com')
        self.assertEqual(conf.email.smtp_port.contents[0], '25')
        self.assertEqual(conf.email.from_email.contents[0], 'user@pyjstack.com')

        for tag in conf.to_email.email:
            print(tag)

        self.assertEqual(conf.email.subject.contents[0], 'Email Notification')
        self.assertEqual(conf.email.attachment.contents[0], '/tmp/pyjstack/attachment.tar.gz')


if __name__ == '__main__':
    unittest.main()