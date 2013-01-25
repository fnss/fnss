import unittest
from nose.tools import *
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
        assert_equal('Mbps', self.G.graph['capacity_unit'])
        assert_true(all([self.G.edge[u][v]['capacity'] in [2, 5] 
                         for (u, v) in self.G.edges()]))
    
    def test_capacities_edge_betweenness(self):
        set_capacities_edge_betweenness(self.G, self.capacities)
        assert_true(all([self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges()]))

    def test_capacities_edge_communicability(self):
        set_capacities_edge_communicability(self.G, self.capacities)
        assert_true(all([self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges()]))
            
    def test_capacities_betweenness_gravity(self):
        set_capacities_betweenness_gravity(self.G, self.capacities)
        assert_true(all([self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges()]))
    
    def test_capacities_communicability_gravity(self):
        set_capacities_communicability_gravity(self.G, self.capacities)
        assert_true(all([self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges()]))
            
    def test_capacities_degree_gravity(self):
        set_capacities_degree_gravity(self.G, self.capacities)
        assert_true(all([self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges()]))       
    
    def test_capacities_eigenvector_gravity(self):
        set_capacities_eigenvector_gravity(self.G, self.capacities)
        assert_true(all([self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges()]))
            
    def test_capacities_pagerank_gravity(self):
        set_capacities_pagerank_gravity(self.G, self.capacities)
        assert_true(all([self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges()]))

    def test_capacities_random_uniform(self):
        set_capacities_random_uniform(self.G, self.capacities)
        assert_true(all([self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges()]))

    def test_capacities_random_power_law(self):
        set_capacities_random_power_law(self.G, self.capacities)
        assert_true(all([self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges()]))

    def test_capacities_random_zipf(self):
        assert_raises(ValueError, set_capacities_random_zipf, 
                      self.G, self.capacities, alpha=0)
        assert_raises(ValueError, set_capacities_random_zipf, 
                      self.G, self.capacities, alpha=-0.2)
        set_capacities_random_zipf(self.G, self.capacities, alpha=0.8)
        assert_true(all([self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges()]))
        set_capacities_random_zipf(self.G, self.capacities, alpha=1.2)
        assert_true(all([self.G.edge[u][v]['capacity'] in self.capacities 
                         for (u, v) in self.G.edges()]))
