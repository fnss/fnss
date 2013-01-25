import unittest
from nose.tools import *
from fnss.topologies.datacenter import *

class DatacenterTopologiesTest(unittest.TestCase):

    def test_fat_tree(self):
        topology = fat_tree_topology(8)
        assert_equal(len(topology), 208)
        
    def test_fat_tree_params(self):
        assert_raises(ValueError, fat_tree_topology, 0)     # zero k
        assert_raises(ValueError, fat_tree_topology, -1)    # negative k
        assert_raises(ValueError, fat_tree_topology, 11)    # odd k
        
    def test_two_tier(self):
        topology = two_tier_topology(10, 20, 30)
        assert_equal(len(topology), 10 + 20 + 20*30)
        
    def test_two_tier_params(self):
        assert_raises(ValueError, two_tier_topology, 0,10,12)
        assert_raises(ValueError, two_tier_topology, 10,0,12)
        assert_raises(ValueError, two_tier_topology, 12,10,0)
        assert_raises(ValueError, two_tier_topology, -1,10,12)
        assert_raises(ValueError, two_tier_topology, 10,-1,12)
        assert_raises(ValueError, two_tier_topology, 12,10,-1)
        
    def test_bcube(self):
        topology = bcube_topology(2, 3)
        assert_equal(topology.number_of_servers(), 16)
        assert_equal(topology.number_of_switches(), 32)
        