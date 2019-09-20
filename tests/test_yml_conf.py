import unittest

from pyjstack.sysconfig import read_yaml_conf
from pyjstack import CONF_YML_PATH


class TestYMLConfMethods(unittest.TestCase):

    def test_read_json_conf(self):
        conf = read_yaml_conf(CONF_YML_PATH)
        self.assertEqual(conf['email']['email'], 'user@gmail.com')
        self.assertEqual(conf['email']['password'], 'secret')
        self.assertEqual(conf['email']['smptp_server'], 'smtp.cloud.com')
