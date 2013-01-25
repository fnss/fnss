import unittest
from nose.tools import *
from fnss.netconfig.buffers import *
from fnss.topologies.topology import Topology, DirectedTopology
from fnss.topologies.randmodels import erdos_renyi_topology
from fnss.netconfig.delays import set_delays_constant
from fnss.netconfig.capacities import set_capacities_random,\
    set_capacities_random_uniform, set_capacities_constant

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # set up topology used for all traffic matrix tests
        cls.G = erdos_renyi_topology(50, 0.4)
        set_capacities_random_uniform(cls.G, [10, 20, 40])
        odd_links = [(u, v) for (u, v) in cls.G.edges() if (u + v) % 2 == 1]
        even_links = [(u, v) for (u, v) in cls.G.edges() if (u + v) % 2 == 0]
        set_delays_constant(cls.G, 2, 'ms', odd_links)
        set_delays_constant(cls.G, 5, 'ms', even_links)
        cls.capacities = [12, 25, 489, 1091]
        
    @classmethod
    def tearDownClass(cls):
        pass
    

    def setUp(self):
        pass


    def tearDown(self):
        clear_buffer_sizes(self.G)
    
    
    def test_buffer_sizes_bw_delay_prod(self):
        set_buffer_sizes_bw_delay_prod(self.G)
        assert_true(all([self.G.edge[u][v]['buffer'] is not None 
                         for (u, v) in self.G.edges()]))

    def test_buffer_sizes_bw_delay_prod_unused_links(self):
        topo = Topology()
        topo.add_edge(1, 2, {'weight': 100})
        topo.add_edge(2, 3, {'weight': 1})
        topo.add_edge(3, 1, {'weight': 1})
        set_capacities_constant(topo, 10)
        set_delays_constant(topo, 2)
        set_buffer_sizes_bw_delay_prod(topo)
        assert_true(all([topo.edge[u][v]['buffer'] is not None 
                         for (u, v) in topo.edges()]))

    def test_buffer_sizes_bw_delay_prod_unused_links_no_return_path(self):
        topo = DirectedTopology()
        topo.add_edge(1, 2, {'weight': 100})
        topo.add_edge(1, 3, {'weight': 1})
        topo.add_edge(3, 2, {'weight': 1})
        set_capacities_constant(topo, 10)
        set_delays_constant(topo, 2)
        assert_raises(ValueError, set_buffer_sizes_bw_delay_prod, topo)


    def test_buffer_sizes_bw_delay_prod_no_return_path(self):
        topo = DirectedTopology()
        topo.add_edge(1, 2, {'weight': 1})
        topo.add_edge(1, 3, {'weight': 1})
        topo.add_edge(3, 2, {'weight': 1})
        set_capacities_constant(topo, 10)
        set_delays_constant(topo, 2)
        assert_raises(ValueError, set_buffer_sizes_bw_delay_prod, topo)

    def test_buffers_size_link_bandwidth(self):
        set_buffer_sizes_link_bandwidth(self.G)
        assert_true(all([self.G.edge[u][v]['buffer'] is not None 
                         for (u, v) in self.G.edges()]))

    def test_buffers_size_constant(self):
        set_buffer_sizes_constant(self.G, 65000, buffer_unit='bytes')
        assert_true(all([self.G.edge[u][v]['buffer'] == 65000 
                         for (u, v) in self.G.edges()]))
        
    def test_get_buffer_sizes(self):
        set_buffer_sizes_constant(self.G, 65000, buffer_unit='bytes')
        buffers = get_buffer_sizes(self.G)
        assert_true(all([buffers[(u, v)] == 65000 for (u, v) in buffers]))
