import sys
if sys.version_info[:2] >= (2, 7):
    import unittest
else:
    try:
        import unittest2 as unittest
    except ImportError:
        raise ImportError("The unittest2 package is needed to run the tests.") 
del sys
from fnss.netconfig.capacities import *
from fnss.topologies.randmodels import erdos_renyi_topology

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
        clear_capacities(self.G)

    
    def test_capacities_constant(self):
        odd_links = [(u, v) for (u, v) in self.G.edges() if (u + v) % 2 == 1]
        even_links = [(u, v) for (u, v) in self.G.edges() if (u + v) % 2 == 0]
        set_capacities_constant(self.G, 2, 'Mbps', odd_links)
        set_capacities_constant(self.G, 5000, 'Kbps', even_links)
        self.assertEqual('Mbps', self.G.graph['capacity_unit'])
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in [2, 5] 
                         for (u, v) in self.G.edges_iter()))
    
    def test_capacities_edge_betweenness(self):
        set_capacities_edge_betweenness(self.G, self.capacities)
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges_iter()))

    def test_capacities_edge_communicability(self):
        set_capacities_edge_communicability(self.G, self.capacities)
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges_iter()))
            
    def test_capacities_betweenness_gravity(self):
        set_capacities_betweenness_gravity(self.G, self.capacities)
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges_iter()))
    
    def test_capacities_communicability_gravity(self):
        set_capacities_communicability_gravity(self.G, self.capacities)
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges_iter()))
        
    def test_capacities_degree_gravity(self):
        set_capacities_degree_gravity(self.G, self.capacities)
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges_iter()))       
    
    def test_capacities_eigenvector_gravity(self):
        set_capacities_eigenvector_gravity(self.G, self.capacities)
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges_iter()))
            
    def test_capacities_pagerank_gravity(self):
        set_capacities_pagerank_gravity(self.G, self.capacities)
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges_iter()))

    def test_capacities_random(self):
        self.assertRaises(ValueError, set_capacities_random,
                          self.G, {10: 0.3, 20: 0.5})
        self.assertRaises(ValueError, set_capacities_random,
                          self.G, {10: 0.3, 20: 0.8})
        set_capacities_random(self.G, {10: 0.3, 20: 0.7})
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in (10, 20) 
                         for (u, v) in self.G.edges_iter()))
        
        
    def test_capacities_random_uniform(self):
        set_capacities_random_uniform(self.G, self.capacities)
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges_iter()))

    def test_capacities_random_power_law(self):
        set_capacities_random_power_law(self.G, self.capacities)
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges_iter()))

    def test_capacities_random_zipf(self):
        self.assertRaises(ValueError, set_capacities_random_zipf, 
                      self.G, self.capacities, alpha=0)
        self.assertRaises(ValueError, set_capacities_random_zipf, 
                      self.G, self.capacities, alpha=-0.2)
        set_capacities_random_zipf(self.G, self.capacities, alpha=0.8)
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges_iter()))
        clear_capacities(self.G)
        set_capacities_random_zipf(self.G, self.capacities, alpha=1.2)
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges_iter()))
    
    def test_capacities_random_zipf_mandlebrot(self):
        self.assertRaises(ValueError, set_capacities_random_zipf_mandelbrot, 
                      self.G, self.capacities, alpha=0)
        self.assertRaises(ValueError, set_capacities_random_zipf_mandelbrot, 
                      self.G, self.capacities, alpha=-0.2)
        self.assertRaises(ValueError, set_capacities_random_zipf_mandelbrot, 
                      self.G, self.capacities, alpha=0.2, q=-0.3)
        # test with alpha=0.8 and q=2.5
        set_capacities_random_zipf_mandelbrot(self.G, self.capacities,
                                              alpha=0.8, q=2.5)
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in self.capacities 
                        for (u, v) in self.G.edges_iter()))
        clear_capacities(self.G)
        # test with alpha=1.2 and q=0.4
        set_capacities_random_zipf_mandelbrot(self.G, self.capacities,
                                              alpha=1.2, q=0.4)
        self.assertTrue(all(self.G.edge[u][v]['capacity'] in self.capacities 
                        for (u, v) in self.G.edges_iter()))
