from nose.tools import *
import unittest
from os import environ, path
from fnss.traffic.trafficmatrices import *
from fnss import erdos_renyi_topology, set_capacities_random, set_capacities_constant, ring_topology


TMP_DIR = environ['test.tmp.dir'] if 'test.tmp.dir' in environ else None


class Test(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        # set up topology used for all traffic matrix tests
        cls.G = erdos_renyi_topology(20, 0.2)
        set_capacities_random(cls.G, {10: 0.5, 20: 0.3, 40: 0.2}, 
                              capacity_unit='Mbps')

    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_traffic_matrix_class(self):
        tm = TrafficMatrix(volume_unit='Mbps')
        tm.add_flow(1, 2, 1000)
        tm.add_flow(1, 3, 1500)
        tm.add_flow(3, 'Four', 4000)
        tm[(4, 5)] = 3000
        tm[('Orig', 'Dest')] = 3000
        assert_equal(tm[(1, 3)], 1500)
        assert_equal(tm.flow[1][3], 1500)
        assert_equal(tm.flows()[(1, 3)], 1500)
        assert_equal(5, len(tm))
        flow = tm.pop_flow(1, 2)
        assert_equal(1000, flow)
        del tm[(1, 3)]
        assert_equal(3, len(tm))
        assert_false(1 in tm.flow)
        assert_false((1, 3) in tm)


    def test_traffic_matrix_sequence_class(self):
        tms = TrafficMatrixSequence()
        tm1 = TrafficMatrix(volume_unit='Mbps')
        tm1.add_flow(1, 2, 1000)
        tm1.add_flow(1, 3, 1500)
        tm1.add_flow(3, 4, 4000)
        tm2 = TrafficMatrix(volume_unit='Mbps')
        tm2.add_flow(1, 2, 2000)
        tm2.add_flow(1, 3, 3500)
        tm2.add_flow(3, 4, 5000)
        tm3 = TrafficMatrix(volume_unit='Mbps')
        tm3.add_flow(1, 2, 5000)
        tm3.add_flow(1, 3, 6500)
        tm3.add_flow(3, 4, 7000)
        tms.append(tm1)
        tms.append(tm2)
        tms.append(tm3)
        assert_equal(1000, tms[0][(1, 2)])
        assert_equal(1000, tms[0].flow[1][2])
        assert_equal(1000, tms.get(0)[(1, 2)])
        assert_equal(1000, tms.get(0).flows()[(1, 2)])
        assert_equal(3, len(tms))
        del tms[0]
        assert_equal(2, len(tms))
        
        
    def test_link_loads(self):
        topo = ring_topology(5)
        set_capacities_constant(topo, 100, capacity_unit='Mbps')
        tm = TrafficMatrix(volume_unit='Mbps')
        tm.add_flow(0, 1, 20)
        tm.add_flow(1, 0, 30)
        tm.add_flow(0, 2, 40)
        tm.add_flow(1, 4, 70)
        tm.add_flow(4, 2, 50)
        load = link_loads(topo, tm)
        assert_almost_equal(0.6, load[(0, 1)])
        assert_almost_equal(1.0, load[(1, 0)])
        assert_almost_equal(0.4, load[(1, 2)])
        assert_almost_equal(0.0, load[(2, 1)])
        assert_almost_equal(0.7, load[(0, 4)])
        assert_almost_equal(0.5, load[(4, 3)])

        
    def test_static_traffic_matrix(self):
        tm = static_traffic_matrix(self.G, 10, 8, max_u=0.9)
        assert_almost_equal(0.9, max(link_loads(self.G, tm).values()))
        assert_less_equal(0, min(link_loads(self.G, tm).values()))


    def test_stationary_traffic_matrix(self):
        tms = stationary_traffic_matrix(self.G, mean=10, stddev=3.5, gamma=5, 
                                        log_psi=-0.3, n=5, max_u=0.9)
        assert_equal(5, len(tms))
        assert_almost_equal(0.9, max([max(link_loads(self.G, tm).values()) for tm in tms]))
        assert_less_equal(0, min([min(link_loads(self.G, tm).values()) for tm in tms]))


    def test_sin_cyclostationary_traffic_matrix(self):
        tms = sin_cyclostationary_traffic_matrix(self.G, 10, 0.2, gamma=0.3, 
                                                log_psi=-0.3, delta=0.2, 
                                                n=24, periods=2, max_u=0.9)
        assert_equal(48, len(tms))
        assert_almost_equal(0.9, max([max(link_loads(self.G, tm).values()) for tm in tms]))
        assert_less_equal(0, min([min(link_loads(self.G, tm).values()) for tm in tms]))
    
    
    @unittest.skipIf(TMP_DIR is None, "Temp folder not present")
    def test_read_write_tm(self):
        tm = static_traffic_matrix(self.G, mean=10, stddev=0.1, max_u=0.9)
        tmp_tm_file = path.join(TMP_DIR, 'tms.xml')
        write_traffic_matrix(tm, tmp_tm_file)
        read_tm = read_traffic_matrix(tmp_tm_file)
        u, v = tm.od_pairs()[2]
        assert_almost_equal(tm[(u, v)], read_tm[(u, v)])

    
    @unittest.skipIf(TMP_DIR is None, "Temp folder not present")
    def test_read_write_tms(self):
        tms = stationary_traffic_matrix(self.G, mean=10, stddev=0.1, gamma=1.2, 
                                        log_psi=-0.3, n=5, max_u=0.9)
        tmp_tms_file = path.join(TMP_DIR, 'tms.xml')
        write_traffic_matrix(tms, tmp_tms_file)
        read_tms = read_traffic_matrix(tmp_tms_file)
        u, v = tms[3].od_pairs()[2]
        assert_almost_equal(tms[3][(u, v)], read_tms[3][(u, v)])


