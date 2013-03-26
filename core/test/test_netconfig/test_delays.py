import sys
from fnss.topologies.simplemodels import star_topology
if sys.version_info[:2] >= (2, 7):
    import unittest
else:
    try:
        import unittest2 as unittest
    except ImportError:
        raise ImportError("The unittest2 package is needed to run the tests.") 
del sys
import networkx as nx
from math import sqrt
from nose.tools import *
from fnss.topologies.randmodels import erdos_renyi_topology, waxman_1_topology, waxman_2_topology
from fnss.netconfig.delays import *

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # set up topology used for all traffic matrix tests
        cls.G = erdos_renyi_topology(50, 0.4)
        
    @classmethod
    def tearDownClass(cls):
        pass
    

    def setUp(self):
        pass


    def tearDown(self):
        clear_delays(self.G)
    
    
    def test_delays_constant(self):
        self.assertRaises(ValueError, set_delays_constant, self.G, 2, 'Km')
        odd_links = [(u, v) for (u, v) in self.G.edges() if (u + v) % 2 == 1]
        even_links = [(u, v) for (u, v) in self.G.edges() if (u + v) % 2 == 0]
        set_delays_constant(self.G, 2, 'ms', odd_links)
        set_delays_constant(self.G, 5000, 'us', even_links)
        self.assertEqual('ms', self.G.graph['delay_unit'])
        self.assertTrue(all(self.G.edge[u][v]['delay'] in [2, 5] 
                         for (u, v) in self.G.edges_iter()))

    def test_delays_geo_distance(self):
        G_len = waxman_1_topology(100, L=5)
        G_xy = waxman_2_topology(100, domain=(0, 0, 3, 4))
        # leave only node coordinate to force calculation of Euclidean distance
        for u, v in G_xy.edges_iter():
            del G_xy.edge[u][v]['length']
        for topo in (G_len, G_xy):
            self.assertRaises(ValueError, set_delays_geo_distance, topo, 2, delay_unit='Km')
            set_delays_geo_distance(topo, 1.2, None, 'ms', links=None)
            delays = nx.get_edge_attributes(topo, 'delay')
            self.assertEqual(topo.number_of_edges(), len(delays))
            self.assertGreaterEqual(1.2*5, max(delays.values()))
            self.assertLessEqual(0, min(delays.values()))
        
    def test_clear_delays(self):
        G = star_topology(12)
        set_delays_constant(G, 1, 'ms', None)
        self.assertEqual(G.number_of_edges(), len(nx.get_edge_attributes(G, 'delay')))
        clear_delays(G)
        self.assertEqual(0, len(nx.get_edge_attributes(G, 'delay')))
