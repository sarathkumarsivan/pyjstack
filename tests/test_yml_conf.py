import unittest

from pyjstack.sysconfig import read_yaml_conf


class TestYMLConfMethods(unittest.TestCase):

    def test_read_json_conf(self):
        conf = read_yaml_conf()

