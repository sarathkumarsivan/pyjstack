import unittest
from pyjstack.sysconfig import read_json_conf
from pyjstack import CONF_JSON_PATH


class TestJSONConfMethods(unittest.TestCase):

    def test_read_json_conf(self):
        conf = read_json_conf(CONF_JSON_PATH)
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
        self.assertEqual(jstack['user'], 'user1')


if __name__ == '__main__':
    unittest.main()
