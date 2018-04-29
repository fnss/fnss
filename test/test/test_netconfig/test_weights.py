import unittest

import networkx as nx

import fnss

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # set up topology used for all traffic matrix tests
        cls.topo = fnss.k_ary_tree_topology(3, 4)
        cls.capacities = [10, 20]
        cls.odd_links = [(u, v) for (u, v) in cls.topo.edges()
                         if (u + v) % 2 == 1]
        cls.even_links = [(u, v) for (u, v) in cls.topo.edges()
                          if (u + v) % 2 == 0]
        fnss.set_capacities_random_uniform(cls.topo, cls.capacities)
        fnss.set_delays_constant(cls.topo, 3, 'ms', cls.odd_links)
        fnss.set_delays_constant(cls.topo, 12, 'ms', cls.even_links)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        fnss.clear_weights(self.topo)

    def test_weights_constant(self):
        fnss.set_weights_constant(self.topo, 2, self.odd_links)
        fnss.set_weights_constant(self.topo, 5, self.even_links)
        self.assertTrue(all(self.topo.adj[u][v]['weight'] in [2, 5]
                            for (u, v) in self.topo.edges()))

    def test_weights_inverse_capacity(self):
        fnss.set_weights_inverse_capacity(self.topo)
        self.assertTrue(all(self.topo.adj[u][v]['weight'] in [1, 2]
                            for (u, v) in self.topo.edges()))

    def test_weights_delays(self):
        fnss.set_weights_delays(self.topo)
        self.assertTrue(all(self.topo.adj[u][v]['weight'] in [1, 4]
                            for (u, v) in self.topo.edges()))

    def test_clear_weights(self):
        # create new topology to avoid parameters pollution
        G = fnss.star_topology(12)
        fnss.set_weights_constant(G, 3, None)
        self.assertEqual(G.number_of_edges(),
                         len(nx.get_edge_attributes(G, 'weight')))
        fnss.clear_weights(G)
        self.assertEqual(0, len(nx.get_edge_attributes(G, 'weight')))
