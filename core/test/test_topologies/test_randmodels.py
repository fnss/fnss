import unittest
import networkx as nx
from nose.tools import *
from fnss.topologies.randmodels import *


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_erdos_renyi_topology(self):
        topology = erdos_renyi_topology(1000, 0.2)
        assert_equal(1000, topology.number_of_nodes())
        assert_raises(ValueError, erdos_renyi_topology, -1, 0.2)
        assert_raises(ValueError, erdos_renyi_topology, 40, 1.2)
        assert_raises(ValueError, erdos_renyi_topology, 50, -0.2)
    
    def test_waxman_1_topology(self):
        assert_raises(ValueError, waxman_1_topology, 0, 0.5, 0.5, 10)
        assert_raises(ValueError, waxman_1_topology, 10, 0, 0.5, 10)
        assert_raises(ValueError, waxman_1_topology, 10, 0.5, 0.5, 0)
        assert_raises(ValueError, waxman_1_topology, 10, 0.5, 0, 10)
        topology = waxman_1_topology(200, alpha=0.5, beta=0.6, L=20)
        assert_equal(200, topology.number_of_nodes())
        length = nx.get_edge_attributes(topology, 'length')
        assert_greater_equal(20, max(length.values()))
        assert_less_equal(0, min(length.values()))
        
    def test_waxman_2_topology(self):
        assert_raises(ValueError, waxman_2_topology, 0, 0.5, 0.6)
        assert_raises(ValueError, waxman_2_topology, 10, 0, 0.5)
        assert_raises(ValueError, waxman_2_topology, 10, 0.4, 0)
        assert_raises(ValueError, waxman_2_topology, 10, 0.5, 0.3, (1.2, -2, 1, 2))
        assert_raises(ValueError, waxman_2_topology, 10, 0.5, 0.3, (-1, 3, 1, 2))
        topology = waxman_2_topology(200, alpha=0.5, beta=0.6, domain=(-1, -2, 1, 2))
        assert_equal(200, topology.number_of_nodes())
        # test all nodes have longitude and latitude attribute
        x = nx.get_node_attributes(topology, 'longitude')
        y = nx.get_node_attributes(topology, 'latitude')
        assert_equal(topology.number_of_nodes(), len(x))
        assert_equal(topology.number_of_nodes(), len(y))
        # test all edges have length attribute
        length = nx.get_edge_attributes(topology, 'length')
        assert_equal(topology.number_of_edges(), len(length))
        # test node coordinates are within predefined domain
        assert_less_equal(-1, min(x.values()))
        assert_less_equal(-2, min(y.values()))
        assert_greater_equal(1, max(x.values()))
        assert_greater_equal(2, max(y.values()))
        
    def test_barabasi_albert_topology(self):
        assert_raises(ValueError, barabasi_albert_topology, 0, 20, 30)
        assert_raises(ValueError, barabasi_albert_topology, 50, 40, 20)
        assert_raises(ValueError, barabasi_albert_topology, 10, 40, 20)
        assert_raises(ValueError, barabasi_albert_topology, 50, -1, 20)
        #G = barabasi_albert_topology(50, 21, 31)
        #assert_equal(50, G.number_of_nodes())
        pass
        
    def test_extended_barabasi_albert_topology(self):
        assert_raises(ValueError, extended_barabasi_albert_topology, 0, 20, 30, 0.2, 0.3)
        assert_raises(ValueError, extended_barabasi_albert_topology, 60, 30, 20, 0.2, 0.3)
        assert_raises(ValueError, extended_barabasi_albert_topology, 60, 20, 30, 0.6, 0.7)
        #G = extended_barabasi_albert_topology(50, 21, 31, 0.2, 0.3)
        #assert_equal(50, G.number_of_nodes())
        pass
    
    def test_glp_topology(self):
        assert_raises(ValueError, glp_topology, 0, 20, 30, 0.4, -0.5)
        assert_raises(ValueError, glp_topology, 100, 30, 20, 0.4, -0.5)
        assert_raises(ValueError, glp_topology, 0, 30, 20, -1, -0.5)
        assert_raises(ValueError, glp_topology, 0, 30, 20, 0.2, -2)
        #topology = glp_topology(200, m, m0, p, beta, seed)