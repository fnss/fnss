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
from fnss.topologies import k_ary_tree_topology, waxman_1_topology, waxman_2_topology
from fnss.netconfig.delays import *

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass
        
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_delays_constant(self):
        topo = k_ary_tree_topology(3, 4)
        self.assertRaises(ValueError, set_delays_constant, topo, 2, 'Km')
        odd_links = [(u, v) for (u, v) in topo.edges_iter()
                     if (u + v) % 2 == 1]
        even_links = [(u, v) for (u, v) in topo.edges_iter()
                      if (u + v) % 2 == 0]
        set_delays_constant(topo, 2, 'ms', odd_links)
        set_delays_constant(topo, 5000, 'us', even_links)
        self.assertEqual('ms', topo.graph['delay_unit'])
        self.assertTrue(all(topo.edge[u][v]['delay'] in [2, 5] 
                         for (u, v) in topo.edges_iter()))

    def test_delays_geo_distance(self):
        specific_delay = 1.2
        L = 5
        G_len = waxman_1_topology(100, L=L)
        G_xy = waxman_2_topology(100, domain=(0, 0, 3, 4))
        # leave only node coordinate to force calculation of Euclidean distance
        for u, v in G_xy.edges_iter():
            del G_xy.edge[u][v]['length']
        for topo in (G_len, G_xy):
            self.assertRaises(ValueError,set_delays_geo_distance,
                              topo, 2, delay_unit='Km')
            set_delays_geo_distance(topo, specific_delay,
                                    None, 'ms', links=None)
            delays = nx.get_edge_attributes(topo, 'delay')
            self.assertEqual(topo.number_of_edges(), len(delays))
            self.assertGreaterEqual(specific_delay*L, max(delays.values()))
            self.assertLessEqual(0, min(delays.values()))
        
    def test_clear_delays(self):
        topo = star_topology(12)
        set_delays_constant(topo, 1, 'ms', None)
        self.assertEqual(topo.number_of_edges(),
                         len(nx.get_edge_attributes(topo, 'delay')))
        clear_delays(topo)
        self.assertEqual(0, len(nx.get_edge_attributes(topo, 'delay')))
