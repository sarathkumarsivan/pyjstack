import unittest

from pyjstack.sysconfig import read_xml_conf


class TestXMLConfMethods(unittest.TestCase):

    def test_read_json_conf(self):
        conf = read_xml_conf()