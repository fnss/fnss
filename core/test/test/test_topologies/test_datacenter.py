import unittest

import fnss

class DatacenterTopologiesTest(unittest.TestCase):

    def test_datacenter_topology_class(self):
        topology = fnss.DatacenterTopology()
        switch_list = [1, 2 , 3]
        host_list = [4, 5, 6, 7]
        others_list = [8, 9]
        for node in switch_list:
            topology.add_node(node, type='switch')
        for node in host_list:
            topology.add_node(node, type='host')
        for node in others_list:
            topology.add_node(node, type='other')
        self.assertEquals(switch_list, topology.switches())
        self.assertEquals(host_list, topology.hosts())
        self.assertEquals(len(switch_list), topology.number_of_switches())
        self.assertEquals(len(host_list), topology.number_of_hosts())

    def test_fat_tree(self):
        topology = fnss.fat_tree_topology(8)
        self.assertEqual(len(topology), 208)

    def test_fat_tree_params(self):
        self.assertRaises(ValueError, fnss.fat_tree_topology, 0)  # zero k
        self.assertRaises(ValueError, fnss.fat_tree_topology, -1)  # negative k
        self.assertRaises(ValueError, fnss.fat_tree_topology, 11)  # odd k

    def test_two_tier(self):
        topology = fnss.two_tier_topology(10, 20, 30)
        self.assertEqual(len(topology), 10 + 20 + 20 * 30)
        self.assertEqual(topology.number_of_hosts(), 20 * 30)
        self.assertEqual(topology.number_of_switches(), 10 + 20)

    def test_two_tier_params(self):
        self.assertRaises(ValueError, fnss.two_tier_topology, 0, 10, 12)
        self.assertRaises(ValueError, fnss.two_tier_topology, 10, 0, 12)
        self.assertRaises(ValueError, fnss.two_tier_topology, 12, 10, 0)
        self.assertRaises(ValueError, fnss.two_tier_topology, -1, 10, 12)
        self.assertRaises(ValueError, fnss.two_tier_topology, 10, -1, 12)
        self.assertRaises(ValueError, fnss.two_tier_topology, 12, 10, -1)

    def test_three_tier(self):
        topology = fnss.three_tier_topology(10, 20, 5, 6)
        self.assertEqual(len(topology), 10 + 20 + 20 * 5 + 20 * 5 * 6)
        self.assertEqual(topology.number_of_hosts(), 20 * 5 * 6)
        self.assertEqual(topology.number_of_switches(), 10 + 20 + 20 * 5)

    def test_three_tier_params(self):
        self.assertRaises(ValueError, fnss.three_tier_topology, 0, 10, 12, 20)
        self.assertRaises(ValueError, fnss.three_tier_topology, 10, 0, 12, 20)
        self.assertRaises(ValueError, fnss.three_tier_topology, 12, 10, 0, 20)
        self.assertRaises(ValueError, fnss.three_tier_topology, 12, 10, 10, 0)
        self.assertRaises(ValueError, fnss.three_tier_topology, -1, 10, 12, 20)
        self.assertRaises(ValueError, fnss.three_tier_topology, 10, -1, 12, 20)
        self.assertRaises(ValueError, fnss.three_tier_topology, 12, 10, -1, 20)
        self.assertRaises(ValueError, fnss.three_tier_topology, 12, 10, 10, -1)

    def test_bcube(self):
        topology = fnss.bcube_topology(2, 3)
        self.assertEqual(topology.number_of_hosts(), 16)
        self.assertEqual(topology.number_of_switches(), 32)

    def test_bcube_params(self):
        self.assertIsNotNone(fnss.bcube_topology(1, 0))
        self.assertRaises(ValueError, fnss.bcube_topology, -1, 2)
        self.assertRaises(ValueError, fnss.bcube_topology, 0, 0)
        self.assertRaises(ValueError, fnss.bcube_topology, 0, 3)
        self.assertRaises(ValueError, fnss.bcube_topology, -1, 4)
