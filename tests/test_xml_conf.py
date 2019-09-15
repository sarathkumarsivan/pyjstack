import unittest

from pyjstack.sysconfig import read_xml_conf
from pyjstack import CONF_INI_PATH


class TestXMLConfMethods(unittest.TestCase):

    def test_read_json_conf(self):
        conf = read_xml_conf(CONF_INI_PATH)