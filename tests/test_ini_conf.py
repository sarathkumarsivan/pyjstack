import unittest
from pyjstack.configurer import read_ini_conf


class TestINIConfMethods(unittest.TestCase):

    def test_read_ini_conf(self):
        conf = read_ini_conf("conf/pyjstack.ini")
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
