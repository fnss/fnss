import unittest
from nose.tools import *
from fnss.topologies.randmodels import erdos_renyi_topology
from fnss.netconfig.capacities import set_capacities_random_uniform
from fnss.netconfig.delays import set_delays_constant
from fnss.netconfig.weights import *

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # set up topology used for all traffic matrix tests
        cls.G = erdos_renyi_topology(50, 0.4)
        cls.capacities = [10, 20]
        odd_links = [(u, v) for (u, v) in cls.G.edges() if (u + v) % 2 == 1]
        even_links = [(u, v) for (u, v) in cls.G.edges() if (u + v) % 2 == 0]
        set_weights_constant(cls.G, 2, odd_links)
        set_weights_constant(cls.G, 5, even_links)
        set_capacities_random_uniform(cls.G, cls.capacities)
        set_delays_constant(cls.G, 3, 'ms', odd_links)
        set_delays_constant(cls.G, 12, 'ms', even_links)
    @classmethod
    def tearDownClass(cls):
        pass
    

    def setUp(self):
        pass


    def tearDown(self):
        pass
    
    def test_weights_constant(self):
        assert_true(all([self.G.edge[u][v]['weight'] in [2, 5] 
                         for (u, v) in self.G.edges()]))

    def test_weights_inverse_capacity(self):
        set_weights_inverse_capacity(self.G)
        assert_true(all([self.G.edge[u][v]['weight'] in [1, 2] 
                         for (u, v) in self.G.edges()]))
        
    def test_weights_delays(self):
        set_weights_delays(self.G)
        assert_true(all([self.G.edge[u][v]['weight'] in [1, 4] 
                         for (u, v) in self.G.edges()]))