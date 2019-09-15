import unittest

from pyjstack.sysconfig import read_yaml_conf
from pyjstack import CONF_INI_PATH


class TestYMLConfMethods(unittest.TestCase):

    def test_read_json_conf(self):
        conf = read_yaml_conf(CONF_INI_PATH)

