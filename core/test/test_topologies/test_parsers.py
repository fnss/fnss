from os import environ, path
from re import findall
import sys
if sys.version_info[:2] >= (2, 7):
    import unittest
else:
    try:
        import unittest2 as unittest
    except ImportError:
        raise ImportError("The unittest2 package is needed to run the tests.") 
del sys
import networkx as nx
from fnss.topologies.parsers import *
from fnss.topologies.topology import Topology

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
        self.assertEqual(size, topology.number_of_nodes())
        self.assertEqual(3, topology.degree(57))


    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_caida_as_relationships(self):
        caida_file = path.join(RES_DIR,'caida-as-rel.txt')
        topology = parse_caida_as_relationships(caida_file)
        self.assertEqual(41203, topology.number_of_nodes())
        self.assertEqual(121309, topology.number_of_edges())
        self.assertEqual('customer',topology.edge[263053][28163]['type'])


    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_inet(self):
        inet_file = path.join(RES_DIR,'inet.txt')
        topology = parse_inet(inet_file)
        self.assertEqual(3500, topology.number_of_nodes())
        self.assertEqual(6146, topology.number_of_edges())
        
    @unittest.skipIf(RES_DIR is None, "Resources folder not present")
    def test_parse_topology_zoo(self):
        topozoo_file = path.join(RES_DIR,'topozoo-arnes.graphml')
        topology = parse_topology_zoo(topozoo_file)
        self.assertEqual(type(topology), Topology)
        self.assertFalse(topology.is_multigraph())
        self.assertEqual(34, topology.number_of_nodes())
        self.assertEqual(46, topology.number_of_edges())
    
    
        