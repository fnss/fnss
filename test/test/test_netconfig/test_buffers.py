import pytest

import fnss
from fnss.util import extend_link_with_0_key


class Test:
    topo = fnss.glp_topology(n=100, m=1, m0=10, p=0.2, beta=-2, seed=1)
    fnss.set_capacities_random_uniform(topo, [10, 20, 40])
    odd_links = [(u, v) for (u, v) in topo.edges()
                 if (u + v) % 2 == 1]
    even_links = [(u, v) for (u, v) in topo.edges()
                  if (u + v) % 2 == 0]
    fnss.set_delays_constant(topo, 2, 'ms', odd_links)
    fnss.set_delays_constant(topo, 5, 'ms', even_links)
    capacities = [12, 25, 489, 1091]

    @pytest.fixture(autouse=True)
    def clear_capacities(self):
        yield
        fnss.clear_buffer_sizes(self.topo)

    def test_buffer_sizes_bw_delay_prod(self):
        fnss.set_buffer_sizes_bw_delay_prod(self.topo)
        assert all(data_dict['buffer'] is not None
                   for data_dict in self.topo.edges.values())

    def test_buffer_sizes_bw_delay_prod_unused_links(self):
        topo = fnss.Topology()
        topo.add_edge(1, 2, weight=100)
        topo.add_edge(2, 3, weight=1)
        topo.add_edge(3, 1, weight=1)
        fnss.set_capacities_constant(topo, 10)
        fnss.set_delays_constant(topo, 2)
        fnss.set_buffer_sizes_bw_delay_prod(topo)
        assert all(data_dict is not None
                   for data_dict in topo.edges.values())

    def test_buffer_sizes_bw_delay_prod_unused_links_no_return_path(self):
        topo = fnss.DirectedTopology()
        topo.add_edge(1, 2, weight=100)
        topo.add_edge(1, 3, weight=1)
        topo.add_edge(3, 2, weight=1)
        fnss.set_capacities_constant(topo, 10)
        fnss.set_delays_constant(topo, 2)
        with pytest.raises(ValueError):
            fnss.set_buffer_sizes_bw_delay_prod(topo)

    def test_buffer_sizes_bw_delay_prod_no_return_path(self):
        topo = fnss.DirectedTopology()
        topo.add_edge(1, 2, weight=1)
        topo.add_edge(1, 3, weight=1)
        topo.add_edge(3, 2, weight=1)
        fnss.set_capacities_constant(topo, 10)
        fnss.set_delays_constant(topo, 2)
        with pytest.raises(ValueError):
            fnss.set_buffer_sizes_bw_delay_prod(topo)

    def test_buffers_size_link_bandwidth(self):
        fnss.set_buffer_sizes_link_bandwidth(self.topo)
        assert all(data_dict['buffer'] is not None
                   for data_dict in self.topo.edges.values())

    def test_buffers_size_link_bandwidth_default_size(self):
        topo = fnss.line_topology(4)

        def edges(u, v):
            return topo.edges[extend_link_with_0_key(topo, u, v)]

        fnss.set_capacities_constant(topo, 8, 'Mbps', [(0, 1)])
        fnss.set_capacities_constant(topo, 16, 'Mbps', [(1, 2)])
        fnss.set_buffer_sizes_link_bandwidth(topo, buffer_unit='bytes', default_size=10)
        assert topo.graph['buffer_unit'] == 'bytes'
        assert edges(0, 1)['buffer'] == 1000000
        assert edges(1, 2)['buffer'] == 2000000
        assert edges(2, 3)['buffer'] == 10
        fnss.clear_buffer_sizes(topo)
        assert 'capacity' not in edges(2, 3)
        with pytest.raises(ValueError):
            fnss.set_buffer_sizes_link_bandwidth(topo)

    def test_buffers_size_constant(self):
        fnss.set_buffer_sizes_constant(self.topo, 65000, buffer_unit='bytes')
        assert all(data_dict['buffer'] == 65000
                   for data_dict in self.topo.edges.values())

    def test_buffers_size_constant_unit_mismatch(self):
        # If I try to set buffer sizes to some interfaces using a unit and some
        # other interfaces already have buffer sizes assigned using a different
        # unit, then raise an error and ask to use the unit previously used
        topo = fnss.line_topology(3)
        fnss.set_buffer_sizes_constant(topo, 10, 'packets', [(0, 1)])
        with pytest.raises(ValueError):
            fnss.set_buffer_sizes_constant(topo, 200, 'bytes', [(1, 2)])

    def test_get_buffer_sizes(self):
        fnss.set_buffer_sizes_constant(self.topo, 65000, buffer_unit='bytes')
        buffers = fnss.get_buffer_sizes(self.topo)
        assert sum(buffer_size == 65000 for buffer_size in buffers.values()) == len(self.topo.edges)
