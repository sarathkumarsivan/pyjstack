import unittest

from pyjstack.sysconfig import read_xml_conf
from pyjstack import CONF_XML_PATH


class TestXMLConfMethods(unittest.TestCase):

    def test_read_json_conf(self):
        conf = read_xml_conf(CONF_XML_PATH)
        print(conf.email.email)
        print(conf.email.password)


if __name__ == '__main__':
    unittest.main()