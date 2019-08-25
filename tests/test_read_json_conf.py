import unittest
from pyjstack.configurer import read_json_conf


class TestConfMethods(unittest.TestCase):

    def test_read_json_conf(self):
        conf = read_json_conf("conf/pyjstack.json")
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
        self.assertEqual(email['pid'], '10023')
        self.assertEqual(email['count'], '12')
        self.assertEqual(email['delay'], '2')


if __name__ == '__main__':
    unittest.main()