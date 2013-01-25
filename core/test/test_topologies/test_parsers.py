from os import environ, path
from re import findall
import unittest
import networkx as nx
from nose.tools import *
from fnss.topologies.parsers import *

RES_DIR = environ['test.res.dir'] if 'test.res.dir' in environ else None

class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_ashiip(self):
        ashiip_file = path.join(RES_DIR, 'ashiip.txt')
        topology = parse_ashiip(ashiip_file)
        with open(ashiip_file, "r") as f:
            for line in f.readlines():
                if line.startswith(' Size :'):
                    size = int(findall('\d+', line)[0])
                    break
        print("Expected number of nodes: ", size)
        print("Actual number of nodes: ", topology.number_of_nodes())
        assert_equal(size, topology.number_of_nodes())
        assert_equal(3, topology.degree(57))


    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_caida_as_relationships(self):
        caida_file = path.join(RES_DIR,'caida-as-rel.txt')
        topology = parse_caida_as_relationships(caida_file)
        assert_equal(41203, topology.number_of_nodes())
        assert_equal(121309, topology.number_of_edges())
        assert_equal('customer',topology.edge[263053][28163]['type'])


    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_inet(self):
        inet_file = path.join(RES_DIR,'inet.txt')
        topology = parse_inet(inet_file)
        assert_equal(3500, topology.number_of_nodes())
        assert_equal(6146, topology.number_of_edges())
    
    
        