import unittest

import networkx as nx
import fnss

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_erdos_renyi_topology(self):
        topology = fnss.erdos_renyi_topology(1000, 0.2)
        topology_fast = fnss.erdos_renyi_topology(1000, 0.2, fast=True)
        for t in (topology, topology_fast):
            self.assertEqual(1000, t.number_of_nodes())
        self.assertRaises(ValueError, fnss.erdos_renyi_topology, -1, 0.2)
        self.assertRaises(ValueError, fnss.erdos_renyi_topology, 40, 1.2)
        self.assertRaises(ValueError, fnss.erdos_renyi_topology, 50, -0.2)

    def test_erdos_renyi_topology_no_seed(self):
        a = fnss.erdos_renyi_topology(100, 0.2)
        b = fnss.erdos_renyi_topology(100, 0.2)
        self.assertNotEqual(set(a.edges()), set(b.edges()))

    def test_erdos_renyi_topology_constant_seed(self):
        a = fnss.erdos_renyi_topology(100, 0.2, seed=1)
        b = fnss.erdos_renyi_topology(100, 0.2, seed=2)
        c = fnss.erdos_renyi_topology(100, 0.2, seed=1)
        self.assertEqual(set(a.edges()), set(c.edges()))
        self.assertNotEqual(set(a.edges()), set(b.edges()))

    def test_erdos_renyi_topology_zero_seed(self):
        a = fnss.erdos_renyi_topology(100, 0.2, seed=0)
        b = fnss.erdos_renyi_topology(100, 0.2, seed=0)
        self.assertEqual(set(a.edges()), set(b.edges()))

    def test_fast_erdos_renyi_topology_no_seed(self):
        a = fnss.erdos_renyi_topology(100, 0.2, fast=True)
        b = fnss.erdos_renyi_topology(100, 0.2, fast=True)
        self.assertNotEqual(set(a.edges()), set(b.edges()))

    def test_fast_erdos_renyi_topology_constant_seed(self):
        a = fnss.erdos_renyi_topology(100, 0.2, fast=True, seed=1)
        b = fnss.erdos_renyi_topology(100, 0.2, fast=True, seed=2)
        c = fnss.erdos_renyi_topology(100, 0.2, fast=True, seed=1)
        self.assertEqual(set(a.edges()), set(c.edges()))
        self.assertNotEqual(set(a.edges()), set(b.edges()))

    def test_fast_erdos_renyi_topology_zero_seed(self):
        a = fnss.erdos_renyi_topology(100, 0.2, fast=True, seed=0)
        b = fnss.erdos_renyi_topology(100, 0.2, fast=True, seed=0)
        self.assertEqual(set(a.edges()), set(b.edges()))

    def test_waxman_1_topology(self):
        self.assertRaises(ValueError, fnss.waxman_1_topology, 0, 0.5, 0.5, 10)
        self.assertRaises(ValueError, fnss.waxman_1_topology, 10, 0, 0.5, 10)
        self.assertRaises(ValueError, fnss.waxman_1_topology, 10, 0.5, 0.5, 0)
        self.assertRaises(ValueError, fnss.waxman_1_topology, 10, 0.5, 0, 10)
        topology = fnss.waxman_1_topology(200, alpha=0.5, beta=0.6, L=20)
        self.assertEqual(200, topology.number_of_nodes())
        length = nx.get_edge_attributes(topology, 'length')
        self.assertGreaterEqual(20, max(length.values()))
        self.assertLessEqual(0, min(length.values()))

    def test_waxman_1_topology_no_seed(self):
        a = fnss.waxman_1_topology(100, alpha=0.5, beta=0.6, L=20)
        b = fnss.waxman_1_topology(100, alpha=0.5, beta=0.6, L=20)
        self.assertNotEqual(set(a.edges()), set(b.edges()))

    def test_waxman_1_topology_constant_seed(self):
        a = fnss.waxman_1_topology(100, alpha=0.5, beta=0.6, L=20, seed=1)
        b = fnss.waxman_1_topology(100, alpha=0.5, beta=0.6, L=20, seed=2)
        c = fnss.waxman_1_topology(100, alpha=0.5, beta=0.6, L=20, seed=1)
        self.assertEqual(set(a.edges()), set(c.edges()))
        self.assertNotEqual(set(a.edges()), set(b.edges()))

    def test_waxman_1_topology_zero_seed(self):
        a = fnss.waxman_1_topology(100, alpha=0.5, beta=0.6, L=20, seed=0)
        b = fnss.waxman_1_topology(100, alpha=0.5, beta=0.6, L=20, seed=0)
        self.assertEqual(set(a.edges()), set(b.edges()))

    def test_waxman_2_topology(self):
        self.assertRaises(ValueError, fnss.waxman_2_topology, 0, 0.5, 0.6)
        self.assertRaises(ValueError, fnss.waxman_2_topology, 10, 0, 0.5)
        self.assertRaises(ValueError, fnss.waxman_2_topology, 10, 0.4, 0)
        self.assertRaises(ValueError, fnss.waxman_2_topology, 10, 0.5, 0.3, (1.2, -2, 1, 2))
        self.assertRaises(ValueError, fnss.waxman_2_topology, 10, 0.5, 0.3, (-1, 3, 1, 2))
        self.assertRaises(ValueError, fnss.waxman_2_topology, 10, 0.5, 0.3, (-1, -2, 1, 2, 5))
        self.assertRaises(ValueError, fnss.waxman_2_topology, 10, 0.5, 0.3, (-1, -2, 1))
        topology = fnss.waxman_2_topology(200, alpha=0.5, beta=0.6, domain=(-1, -2, 1, 2))
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

    def test_waxman_2_topology_no_seed(self):
        a = fnss.waxman_2_topology(100, alpha=0.5, beta=0.6, domain=(-1, -2, 1, 2))
        b = fnss.waxman_2_topology(100, alpha=0.5, beta=0.6, domain=(-1, -2, 1, 2))
        self.assertNotEqual(set(a.edges()), set(b.edges()))

    def test_waxman_2_topology_constant_seed(self):
        a = fnss.waxman_2_topology(100, alpha=0.5, beta=0.6, domain=(-1, -2, 1, 2), seed=1)
        b = fnss.waxman_2_topology(100, alpha=0.5, beta=0.6, domain=(-1, -2, 1, 2), seed=2)
        c = fnss.waxman_2_topology(100, alpha=0.5, beta=0.6, domain=(-1, -2, 1, 2), seed=1)
        self.assertEqual(set(a.edges()), set(c.edges()))
        self.assertNotEqual(set(a.edges()), set(b.edges()))

    def test_waxman_2_topology_zero_seed(self):
        a = fnss.waxman_2_topology(100, alpha=0.5, beta=0.6, domain=(-1, -2, 1, 2), seed=0)
        b = fnss.waxman_2_topology(100, alpha=0.5, beta=0.6, domain=(-1, -2, 1, 2), seed=0)
        self.assertEqual(set(a.edges()), set(b.edges()))

    def test_barabasi_albert_topology(self):
        self.assertRaises(ValueError, fnss.barabasi_albert_topology, 0, 20, 30)
        self.assertRaises(ValueError, fnss.barabasi_albert_topology, 50, 40, 20)
        self.assertRaises(ValueError, fnss.barabasi_albert_topology, 10, 40, 20)
        self.assertRaises(ValueError, fnss.barabasi_albert_topology, 50, -1, 20)
        self.assertRaises(ValueError, fnss.barabasi_albert_topology, 10, 11, 16)
        topology = fnss.barabasi_albert_topology(100, 11, 16)
        self.assertEqual(100, topology.number_of_nodes())

    def test_barabasi_albert_topology_no_seed(self):
        a = fnss.barabasi_albert_topology(100, 11, 16)
        b = fnss.barabasi_albert_topology(100, 11, 16)
        self.assertNotEqual(set(a.edges()), set(b.edges()))

    def test_barabasi_albert_topology_constant_seed(self):
        a = fnss.barabasi_albert_topology(100, 11, 16, seed=1)
        b = fnss.barabasi_albert_topology(100, 11, 16, seed=2)
        c = fnss.barabasi_albert_topology(100, 11, 16, seed=1)
        self.assertEqual(set(a.edges()), set(c.edges()))
        self.assertNotEqual(set(a.edges()), set(b.edges()))

    def test_barabasi_albert_topology_zero_seed(self):
        a = fnss.barabasi_albert_topology(100, 11, 16, seed=0)
        b = fnss.barabasi_albert_topology(100, 11, 16, seed=0)
        self.assertEqual(set(a.edges()), set(b.edges()))

    def test_extended_barabasi_albert_topology(self):
        self.assertRaises(ValueError, fnss.extended_barabasi_albert_topology, 0, 20, 30, 0.2, 0.3)
        self.assertRaises(ValueError, fnss.extended_barabasi_albert_topology, 60, 30, 20, 0.2, 0.3)
        self.assertRaises(ValueError, fnss.extended_barabasi_albert_topology, 60, 20, 30, 0.6, 0.7)
        self.assertRaises(ValueError, fnss.extended_barabasi_albert_topology, 20, 11, 16, 1.2, 0.3)
        self.assertRaises(ValueError, fnss.extended_barabasi_albert_topology, 20, 11, 16, 0.3, 1.2)
        self.assertRaises(ValueError, fnss.extended_barabasi_albert_topology, 20, 11, 16, -0.2, 0.3)
        self.assertRaises(ValueError, fnss.extended_barabasi_albert_topology, 20, 11, 16, 0.3, -0.2)
        self.assertRaises(ValueError, fnss.extended_barabasi_albert_topology, 16, 11, 20, 0.2, 0.3)
        topology = fnss.extended_barabasi_albert_topology(100, 11, 16, 0.2, 0.3)
        self.assertEqual(100, topology.number_of_nodes())

    def test_extended_barabasi_albert_topology_no_seed(self):
        a = fnss.extended_barabasi_albert_topology(100, 11, 16, 0.2, 0.3)
        b = fnss.extended_barabasi_albert_topology(100, 11, 16, 0.2, 0.3)
        self.assertNotEqual(set(a.edges()), set(b.edges()))

    def test_extended_barabasi_albert_topology_constant_seed(self):
        a = fnss.extended_barabasi_albert_topology(100, 11, 16, 0.2, 0.3, seed=1)
        b = fnss.extended_barabasi_albert_topology(100, 11, 16, 0.2, 0.3, seed=2)
        c = fnss.extended_barabasi_albert_topology(100, 11, 16, 0.2, 0.3, seed=1)
        self.assertEqual(set(a.edges()), set(c.edges()))
        self.assertNotEqual(set(a.edges()), set(b.edges()))

    def test_extended_barabasi_albert_topology_zero_seed(self):
        a = fnss.extended_barabasi_albert_topology(100, 11, 16, 0.2, 0.3, seed=0)
        b = fnss.extended_barabasi_albert_topology(100, 11, 16, 0.2, 0.3, seed=0)
        self.assertEqual(set(a.edges()), set(b.edges()))

    def test_glp_topology(self):
        self.assertRaises(ValueError, fnss.glp_topology, 0, 20, 30, 0.4, -0.5)
        self.assertRaises(ValueError, fnss.glp_topology, 100, 30, 20, 0.4, -0.5)
        self.assertRaises(ValueError, fnss.glp_topology, 0, 30, 20, -1, -0.5)
        self.assertRaises(ValueError, fnss.glp_topology, 0, 30, 20, 0.2, -2)
        self.assertRaises(ValueError, fnss.glp_topology, 20, 11, 16, -0.5, 0.5)
        self.assertRaises(ValueError, fnss.glp_topology, 20, 11, 16, 1.5, 0.5)
        topology = fnss.glp_topology(20, 11, 16, 0.5, 0.5)
        self.assertEqual(20, topology.number_of_nodes())

    def test_glp_topology_no_seed(self):
        a = fnss.glp_topology(100, 15, 20, 0.5, 0.5)
        b = fnss.glp_topology(100, 15, 20, 0.5, 0.5)
        self.assertNotEqual(set(a.edges()), set(b.edges()))

    def test_glp_topology_constant_seed(self):
        a = fnss.glp_topology(100, 15, 20, 0.5, 0.5, seed=1)
        b = fnss.glp_topology(100, 15, 20, 0.5, 0.5, seed=2)
        c = fnss.glp_topology(100, 15, 20, 0.5, 0.5, seed=1)
        self.assertEqual(set(a.edges()), set(c.edges()))
        self.assertNotEqual(set(a.edges()), set(b.edges()))

    def test_glp_topology_zero_seed(self):
        a = fnss.glp_topology(100, 15, 20, 0.5, 0.5, seed=0)
        b = fnss.glp_topology(100, 15, 20, 0.5, 0.5, seed=0)
        self.assertEqual(set(a.edges()), set(b.edges()))
