import sys
if sys.version_info[:2] >= (2, 7):
    import unittest
else:
    try:
        import unittest2 as unittest
    except ImportError:
        raise ImportError("The unittest2 package is needed to run the tests.") 
del sys
from nose.tools import *
from fnss.topologies.randmodels import erdos_renyi_topology
from fnss.netconfig.delays import *

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # set up topology used for all traffic matrix tests
        cls.G = erdos_renyi_topology(50, 0.4)
        cls.capacities = [12, 25, 489, 1091]
        
    @classmethod
    def tearDownClass(cls):
        pass
    

    def setUp(self):
        pass


    def tearDown(self):
        clear_delays(self.G)
    
    
    def test_delays_constant(self):
        odd_links = [(u, v) for (u, v) in self.G.edges() if (u + v) % 2 == 1]
        even_links = [(u, v) for (u, v) in self.G.edges() if (u + v) % 2 == 0]
        set_delays_constant(self.G, 2, 'ms', odd_links)
        set_delays_constant(self.G, 5000, 'us', even_links)
        self.assertEqual('ms', self.G.graph['delay_unit'])
        self.assertTrue(all(self.G.edge[u][v]['delay'] in [2, 5] 
                         for (u, v) in self.G.edges_iter()))

