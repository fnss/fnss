import unittest

import networkx as nx

import fnss


class Test(unittest.TestCase):

    # TODO add multigraph tests
    @classmethod
    def setUpClass(cls):
        # set up topology used for all traffic matrix tests
        cls.topo = fnss.k_ary_tree_topology(3, 4)
        cls.capacities = [10, 20]
        cls.odd_links = [link for link in cls.topo.edges
                         if sum(link) % 2 == 1]
        cls.even_links = [link for link in cls.topo.edges
                          if sum(link) % 2 == 0]
        fnss.set_capacities_random_uniform(cls.topo, cls.capacities)
        fnss.set_delays_constant(cls.topo, 3, 'ms', cls.odd_links)
        fnss.set_delays_constant(cls.topo, 12, 'ms', cls.even_links)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_weights_constant(self):
        fnss.set_weights_constant(self.topo, 2, self.odd_links)
        fnss.set_weights_constant(self.topo, 5, self.even_links)
        self.assertTrue(all(data_dict['weight'] in [2, 5]
                            for data_dict in self.topo.edges.values()))

    def test_weights_inverse_capacity(self):
        fnss.set_weights_inverse_capacity(self.topo)
        self.assertTrue(all(data_dict['weight'] in [1, 2]
                            for data_dict in self.topo.edges.values()))

    def test_weights_delays(self):
        fnss.set_weights_delays(self.topo)
        self.assertTrue(all(data_dict['weight'] in [1, 4]
                            for data_dict in self.topo.edges.values()))

    def test_clear_weights(self):
        # create new topology to avoid parameters pollution
        G = fnss.star_topology(12)
        fnss.set_weights_constant(G, 3, None)
        self.assertEqual(G.number_of_edges(),
                         len(nx.get_edge_attributes(G, 'weight')))
        fnss.clear_weights(G)
        self.assertEqual(0, len(nx.get_edge_attributes(G, 'weight')))
