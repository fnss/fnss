from os import path, environ
import sys
if sys.version_info[:2] >= (2, 7):
    import unittest
else:
    try:
        import unittest2 as unittest
    except ImportError:
        raise ImportError("The unittest2 package is needed to run the tests.") 
del sys
from fnss.topologies import *
from fnss.netconfig import *


TMP_DIR = environ['test.tmp.dir'] if 'test.tmp.dir' in environ else None


class Test(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        # set up topology used for all traffic matrix tests
        cls.G = erdos_renyi_topology(10, 0.5)
        set_capacities_random(cls.G, {10: 0.5, 20: 0.3, 40: 0.2}, 
                              capacity_unit='Mbps')
        set_delays_constant(cls.G, 2, delay_unit='ms')
        set_weights_inverse_capacity(cls.G)
        for node in [2, 4, 6]:
            add_stack(cls.G, node, 'tcp', 
                          {'protocol': 'cubic', 'rcvwnd': 1024})
        for node in [2, 4]:
            add_application(cls.G, node, 'client', 
                                {'rate': 100, 'user-agent': 'fnss'})
        add_application(cls.G, 2, 'server', 
                           {'port': 80, 'active': True, 'user-agent': 'fnss'})


    @classmethod
    def tearDownClass(cls):
        pass


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_od_pairs_from_topology_directed(self):
        dir_topology = DirectedTopology()
        dir_topology.add_edge(0, 1)
        dir_topology.add_edge(1, 0)
        dir_topology.add_edge(1, 2)
        dir_topology.add_edge(3, 2)
        dir_topology.add_edge(8, 9)
        expected_od_pairs = [(0, 1), (0, 2), (1, 0), (1, 2), (3, 2), (8, 9)]
        od_pairs = od_pairs_from_topology(dir_topology)
        self.assertEquals(len(expected_od_pairs), len(od_pairs))
        for od in expected_od_pairs:
            self.assertTrue(od in od_pairs)


    def test_od_pairs_from_topology_undirected(self):
        topology = ring_topology(3)
        topology.add_path([7, 8, 9]) # isolated node: no flows from/to this node 
        od_pairs = od_pairs_from_topology(topology)
        expected_od_pairs = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1),
                             (7, 8), (7, 9), (8, 7), (8, 9), (9, 7), (9, 8)]
        self.assertEquals(len(expected_od_pairs), len(od_pairs))
        for od in expected_od_pairs:
            self.assertTrue(od in od_pairs)


    def test_fan_in_out_capacities_directed(self):
        dir_topology = DirectedTopology()
        dir_topology.add_edge(0, 1)
        dir_topology.add_edge(1, 0)
        dir_topology.add_edge(1, 2)
        dir_topology.add_edge(3, 2)
        set_capacities_constant(dir_topology, 10, 'Mbps')
        in_cap, out_cap = fan_in_out_capacities(dir_topology)
        self.assertEquals({0: 10, 1: 10, 2: 20, 3: 0}, in_cap)
        self.assertEquals({0: 10, 1: 20, 2: 0, 3: 10}, out_cap)
        

    def test_fan_in_out_capacities_undirected(self):
        topology = star_topology(3)
        set_capacities_constant(topology, 10, 'Mbps')
        in_cap, out_cap = fan_in_out_capacities(topology)
        self.assertEquals({0: 30, 1: 10, 2: 10, 3: 10}, in_cap)
        self.assertEquals(in_cap, out_cap)


    @unittest.skipIf(TMP_DIR is None, "Temp folder not present")
    def test_read_write_topology(self):
        tmp_topo_file = path.join(TMP_DIR, 'toporw.xml')
        write_topology(self.G, tmp_topo_file)
        self.assertTrue(path.exists(tmp_topo_file))
        read_topo = read_topology(tmp_topo_file)
        self.assertEquals(len(self.G), len(read_topo))
        self.assertEquals(self.G.number_of_edges(), read_topo.number_of_edges())
        self.assertEquals('tcp', get_stack(read_topo, 2)[0])
        self.assertEquals(1024, get_stack(read_topo, 2)[1]['rcvwnd'])
        self.assertEquals('cubic', get_stack(read_topo, 2)[1]['protocol'])
        self.assertEquals(len(get_application_names(self.G, 2)), 
                      len(get_application_names(read_topo, 2)))
        self.assertEquals('fnss', get_application_properties(read_topo, 2, 'server')['user-agent'])
        self.assertEquals([2, 4, 6], [ v for v in read_topo.nodes_iter() if get_stack(read_topo, v) is not None and get_stack(read_topo, v)[0] == 'tcp'])
        self.assertEquals([2, 4], [ v for v in read_topo.nodes_iter() if 'client' in get_application_names(read_topo, v)])
        self.assertEquals([2], [ v for v in read_topo.nodes_iter() if 'server' in get_application_names(read_topo, v)])
