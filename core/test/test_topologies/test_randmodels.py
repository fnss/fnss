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
from fnss.topologies.randmodels import *


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_erdos_renyi_topology(self):
        topology = erdos_renyi_topology(1000, 0.2)
        topology_fast = erdos_renyi_topology(1000, 0.2, fast=True)
        for t in (topology, topology_fast):
            self.assertEqual(1000, t.number_of_nodes())
        self.assertRaises(ValueError, erdos_renyi_topology, -1, 0.2)
        self.assertRaises(ValueError, erdos_renyi_topology, 40, 1.2)
        self.assertRaises(ValueError, erdos_renyi_topology, 50, -0.2)
    
    def test_waxman_1_topology(self):
        self.assertRaises(ValueError, waxman_1_topology, 0, 0.5, 0.5, 10)
        self.assertRaises(ValueError, waxman_1_topology, 10, 0, 0.5, 10)
        self.assertRaises(ValueError, waxman_1_topology, 10, 0.5, 0.5, 0)
        self.assertRaises(ValueError, waxman_1_topology, 10, 0.5, 0, 10)
        topology = waxman_1_topology(200, alpha=0.5, beta=0.6, L=20)
        self.assertEqual(200, topology.number_of_nodes())
        length = nx.get_edge_attributes(topology, 'length')
        self.assertGreaterEqual(20, max(length.values()))
        self.assertLessEqual(0, min(length.values()))
        
    def test_waxman_2_topology(self):
        self.assertRaises(ValueError, waxman_2_topology, 0, 0.5, 0.6)
        self.assertRaises(ValueError, waxman_2_topology, 10, 0, 0.5)
        self.assertRaises(ValueError, waxman_2_topology, 10, 0.4, 0)
        self.assertRaises(ValueError, waxman_2_topology, 10, 0.5, 0.3, (1.2, -2, 1, 2))
        self.assertRaises(ValueError, waxman_2_topology, 10, 0.5, 0.3, (-1, 3, 1, 2))
        self.assertRaises(ValueError, waxman_2_topology, 10, 0.5, 0.3, (-1, -2, 1, 2, 5))
        self.assertRaises(ValueError, waxman_2_topology, 10, 0.5, 0.3, (-1, -2, 1))
        topology = waxman_2_topology(200, alpha=0.5, beta=0.6, domain=(-1, -2, 1, 2))
        self.assertEqual(200, topology.number_of_nodes())
        # test all nodes have longitude and latitude attribute
        x = nx.get_node_attributes(topology, 'longitude')
        y = nx.get_node_attributes(topology, 'latitude')
        self.assertEqual(topology.number_of_nodes(), len(x))
        self.assertEqual(topology.number_of_nodes(), len(y))
        # test all edges have length attribute
        length = nx.get_edge_attributes(topology, 'length')
        self.assertEqual(topology.number_of_edges(), len(length))
        # test node coordinates are within predefined domain
        self.assertLessEqual(-1, min(x.values()))
        self.assertLessEqual(-2, min(y.values()))
        self.assertGreaterEqual(1, max(x.values()))
        self.assertGreaterEqual(2, max(y.values()))
        
    def test_barabasi_albert_topology(self):
        self.assertRaises(ValueError, barabasi_albert_topology, 0, 20, 30)
        self.assertRaises(ValueError, barabasi_albert_topology, 50, 40, 20)
        self.assertRaises(ValueError, barabasi_albert_topology, 10, 40, 20)
        self.assertRaises(ValueError, barabasi_albert_topology, 50, -1, 20)
        self.assertRaises(ValueError, barabasi_albert_topology, 10, 11, 16)
        topology = barabasi_albert_topology(100, 11, 16)
        self.assertEqual(100, topology.number_of_nodes())
        
    def test_extended_barabasi_albert_topology(self):
        self.assertRaises(ValueError, extended_barabasi_albert_topology, 0, 20, 30, 0.2, 0.3)
        self.assertRaises(ValueError, extended_barabasi_albert_topology, 60, 30, 20, 0.2, 0.3)
        self.assertRaises(ValueError, extended_barabasi_albert_topology, 60, 20, 30, 0.6, 0.7)
        self.assertRaises(ValueError, extended_barabasi_albert_topology, 20, 11, 16, 1.2, 0.3)
        self.assertRaises(ValueError, extended_barabasi_albert_topology, 20, 11, 16, 0.3, 1.2)
        self.assertRaises(ValueError, extended_barabasi_albert_topology, 20, 11, 16, -0.2, 0.3)
        self.assertRaises(ValueError, extended_barabasi_albert_topology, 20, 11, 16, 0.3, -0.2)
        self.assertRaises(ValueError, extended_barabasi_albert_topology, 16, 11, 20, 0.2, 0.3)
        topology = extended_barabasi_albert_topology(100, 11, 16, 0.2, 0.3)
        self.assertEqual(100, topology.number_of_nodes())
    
    def test_glp_topology(self):
        self.assertRaises(ValueError, glp_topology, 0, 20, 30, 0.4, -0.5)
        self.assertRaises(ValueError, glp_topology, 100, 30, 20, 0.4, -0.5)
        self.assertRaises(ValueError, glp_topology, 0, 30, 20, -1, -0.5)
        self.assertRaises(ValueError, glp_topology, 0, 30, 20, 0.2, -2)
        self.assertRaises(ValueError, glp_topology, 20, 11, 16, -0.5, 0.5)
        self.assertRaises(ValueError, glp_topology, 20, 11, 16, 1.5, 0.5)
        topology = glp_topology(20, 11, 16, 0.5, 0.5)
        self.assertEqual(20, topology.number_of_nodes())