import unittest

from pyjstack.sysconfig import read_yaml_conf
from pyjstack import CONF_YML_PATH


class TestYMLConfMethods(unittest.TestCase):

    def test_read_json_conf(self):
        conf = read_yaml_conf(CONF_YML_PATH)

        for section in conf:
            print(section)

