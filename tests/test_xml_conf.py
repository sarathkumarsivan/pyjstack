import unittest

from pyjstack.sysconfig import read_xml_conf

CONF_PATH = 'conf/pyjstack-conf.xml'


class TestXMLConfMethods(unittest.TestCase):

    def test_read_json_conf(self):
        conf = read_xml_conf(CONF_PATH)