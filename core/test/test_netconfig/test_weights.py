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
from fnss.topologies import k_ary_tree_topology, star_topology
from fnss.netconfig.capacities import set_capacities_random_uniform
from fnss.netconfig.delays import set_delays_constant
from fnss.netconfig.weights import *

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # set up topology used for all traffic matrix tests
        cls.topo = k_ary_tree_topology(3, 4)
        cls.capacities = [10, 20]
        cls.odd_links = [(u, v) for (u, v) in cls.topo.edges_iter()
                         if (u + v) % 2 == 1]
        cls.even_links = [(u, v) for (u, v) in cls.topo.edges_iter()
                          if (u + v) % 2 == 0]
        set_capacities_random_uniform(cls.topo, cls.capacities)
        set_delays_constant(cls.topo, 3, 'ms', cls.odd_links)
        set_delays_constant(cls.topo, 12, 'ms', cls.even_links)
    
    @classmethod
    def tearDownClass(cls):
        pass
    

    def setUp(self):
        pass

    def tearDown(self):
        clear_weights(self.topo)
    
    def test_weights_constant(self):
        set_weights_constant(self.topo, 2, self.odd_links)
        set_weights_constant(self.topo, 5, self.even_links)
        self.assertTrue(all(self.topo.edge[u][v]['weight'] in [2, 5]
                            for (u, v) in self.topo.edges_iter()))

    def test_weights_inverse_capacity(self):
        set_weights_inverse_capacity(self.topo)
        self.assertTrue(all(self.topo.edge[u][v]['weight'] in [1, 2] 
                            for (u, v) in self.topo.edges_iter()))
        
    def test_weights_delays(self):
        set_weights_delays(self.topo)
        self.assertTrue(all(self.topo.edge[u][v]['weight'] in [1, 4] 
                            for (u, v) in self.topo.edges_iter()))
        
    def test_clear_weights(self):
        G = star_topology(12) # create new topology to avoid params pollution
        set_weights_constant(G, 3, None)
        self.assertEqual(G.number_of_edges(),
                         len(nx.get_edge_attributes(G, 'weight')))
        clear_weights(G)
        self.assertEqual(0, len(nx.get_edge_attributes(G, 'weight')))