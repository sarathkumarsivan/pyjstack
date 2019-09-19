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
        self.assertEqual(conf.jstack.pid.contents[0], '10023')
        self.assertEqual(conf.jstack.count.contents[0], '12')
        self.assertEqual(conf.jstack.delay.contents[0], '2')
        self.assertEqual(conf.jstack.user.contents[0], 'user1')

if __name__ == '__main__':
    unittest.main()