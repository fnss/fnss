import unittest

import networkx as nx

import fnss
from fnss.util import extend_link_with_0_key


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
        topo = fnss.k_ary_tree_topology(3, 4)
        self.assertRaises(ValueError, fnss.set_delays_constant, topo, 2, 'Km')
        odd_links = [(u, v) for (u, v) in topo.edges()
                     if (u + v) % 2 == 1]
        even_links = [(u, v) for (u, v) in topo.edges()
                      if (u + v) % 2 == 0]
        fnss.set_delays_constant(topo, 2, 's', odd_links)
        fnss.set_delays_constant(topo, 5000000, 'us', even_links)
        self.assertEqual('s', topo.graph['delay_unit'])
        self.assertTrue(all(data_dict['delay'] in [2, 5]
                            for data_dict in topo.edges.values()))

    def test_delays_geo_distance(self):
        specific_delay = 1.2
        L = 5
        G_len = fnss.waxman_1_topology(100, L=L)
        G_xy = fnss.waxman_2_topology(100, domain=(0, 0, 3, 4))
        # leave only node coordinate to trigger failure
        for data_dict in G_xy.edges.values():
            del data_dict['length']
        self.assertRaises(ValueError, fnss.set_delays_geo_distance,
                          G_len, 2, delay_unit='Km')
        self.assertRaises(ValueError, fnss.set_delays_geo_distance,
                          G_xy, specific_delay, None, 'ms')
        fnss.set_delays_geo_distance(G_len, specific_delay,
                                None, 'ms', links=None)
        delays = nx.get_edge_attributes(G_len, 'delay')
        self.assertEqual(G_len.number_of_edges(), len(delays))
        self.assertGreaterEqual(specific_delay * L, max(delays.values()))
        self.assertLessEqual(0, min(delays.values()))

    def test_delays_geo_distance_conversions(self):
        topology = fnss.Topology(distance_unit='m')

        def edges(u, v):
            return topology.edges[extend_link_with_0_key(topology, u, v)]

        topology.add_edge(1, 2, length=2000)
        specific_delay = 1.2
        fnss.set_delays_geo_distance(topology, specific_delay, None, 'us')
        self.assertAlmostEqual(edges(1, 2)['delay'], 2400)
        fnss.clear_delays(topology)
        fnss.set_delays_geo_distance(topology, specific_delay, None, 's')
        self.assertAlmostEqual(edges(1, 2)['delay'], 0.0024)

    def test_delays_geo_distance_conversions_partial_assignments(self):
        topology = fnss.Topology(distance_unit='m')

        def edges(u, v):
            return topology.edges[extend_link_with_0_key(topology, u, v)]
        
        topology.add_edge(1, 2, length=2000)
        topology.add_edge(2, 3, length=3000)
        topology.add_edge(3, 4)
        specific_delay = 1.2
        fnss.set_delays_geo_distance(topology, specific_delay,
                                     None, 'us', links=[(1, 2)])
        fnss.set_delays_geo_distance(topology, specific_delay,
                                     3, 's', links=[(2, 3), (3, 4)])
        self.assertEquals(topology.graph['distance_unit'], 'm')
        self.assertEquals(topology.graph['delay_unit'], 'us')
        self.assertAlmostEqual(edges(1, 2)['delay'], 2400)
        self.assertAlmostEqual(edges(2, 3)['delay'], 3600)
        self.assertAlmostEqual(edges(3, 4)['delay'], 3000000)

    def test_delays_geo_distance_conversions_defaults(self):
        topology = fnss.Topology(distance_unit='m')

        def edges(u, v):
            return topology.edges[extend_link_with_0_key(topology, u, v)]

        topology.add_edge(1, 2, length=2000)
        topology.add_edge(2, 3, length=3000)
        topology.add_edge(3, 4)
        specific_delay = 1.2
        fnss.set_delays_geo_distance(topology, specific_delay, 3, 's', None)
        self.assertEquals(topology.graph['distance_unit'], 'm')
        self.assertEquals(topology.graph['delay_unit'], 's')
        self.assertAlmostEqual(edges(1, 2)['delay'], 0.0024)
        self.assertAlmostEqual(edges(2, 3)['delay'], 0.0036)
        self.assertAlmostEqual(edges(3, 4)['delay'], 3)

    def test_clear_delays(self):
        topo = fnss.star_topology(12)
        fnss.set_delays_constant(topo, 1, 'ms', None)
        self.assertEqual(topo.number_of_edges(),
                         len(nx.get_edge_attributes(topo, 'delay')))
        fnss.clear_delays(topo)
        self.assertEqual(0, len(nx.get_edge_attributes(topo, 'delay')))
