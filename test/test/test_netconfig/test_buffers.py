import pytest

import fnss
from fnss import Topology
from fnss.util import extend_link_tuple_to_all_parallel
from test_topologies.test_topology import duplicate_edge, has_parallel_edges
# required import for pytest fixture
# noinspection PyUnresolvedReferences
from test_topologies.test_topology import use_multigraph, topology_converter, topology, dir_topology


class Test:
    topo = None

    _topo_multi = fnss.glp_topology(n=100, m=1, m0=10, p=0.2, beta=-2, seed=1).to_multigraph()
    duplicate_edge_orig, duplicate_edge_new = duplicate_edge(_topo_multi, True)
    duplicate_edge_simple = duplicate_edge_orig[:2]

    fnss.set_capacities_random_uniform(_topo_multi, [10, 20, 40])

    _odd_links = [link for link in _topo_multi.edges if sum(link) % 2 == 1]
    _even_links = [link for link in _topo_multi.edges if sum(link) % 2 == 0]
    fnss.set_delays_constant(_topo_multi, 2, 'ms', _odd_links)
    fnss.set_delays_constant(_topo_multi, 5, 'ms', _even_links)

    _topo_simple = Topology(_topo_multi)

    capacities = [12, 25, 489, 1091]

    @pytest.fixture(autouse=True)
    def init_topo(self, use_multigraph):
        self.topo = self._topo_multi if use_multigraph \
            else self._topo_simple
        fnss.clear_buffer_sizes(self.topo)

        assert self.topo.is_multigraph() == use_multigraph
        assert has_parallel_edges(self.topo) == use_multigraph

        yield

        self.topo = None

    def test_buffer_sizes_bw_delay_prod(self):
        fnss.set_buffer_sizes_bw_delay_prod(self.topo)
        assert all(data_dict['buffer'] is not None
                   for data_dict in self.topo.edges.values())

    def test_buffer_sizes_bw_delay_prod_unused_links(self, topology, use_multigraph):
        # duplicate edge, no effect for simple graphs
        topology.add_edge(1, 2, weight=200)
        topology.add_edge(1, 2, weight=100)

        topology.add_edge(2, 3, weight=1)
        topology.add_edge(3, 1, weight=1)

        assert has_parallel_edges(topology) == use_multigraph

        fnss.set_capacities_constant(topology, 10)
        fnss.set_delays_constant(topology, 2)
        fnss.set_buffer_sizes_bw_delay_prod(topology)
        assert all(data_dict is not None
                   for data_dict in topology.edges.values())

    def test_buffer_sizes_bw_delay_prod_unused_links_no_return_path(self, dir_topology, use_multigraph):
        # duplicate edge, no effect for simple graphs
        dir_topology.add_edge(1, 2, weight=200)
        dir_topology.add_edge(1, 2, weight=100)

        dir_topology.add_edge(1, 3, weight=1)
        dir_topology.add_edge(3, 2, weight=1)

        assert has_parallel_edges(dir_topology) == use_multigraph

        fnss.set_capacities_constant(dir_topology, 10)
        fnss.set_delays_constant(dir_topology, 2)
        with pytest.raises(ValueError):
            fnss.set_buffer_sizes_bw_delay_prod(dir_topology)

    def test_buffer_sizes_bw_delay_prod_no_return_path(self, dir_topology, use_multigraph):
        # duplicate edge, no effect for simple graphs
        dir_topology.add_edge(1, 2, weight=1)
        dir_topology.add_edge(1, 2, weight=1)

        dir_topology.add_edge(1, 3, weight=1)
        dir_topology.add_edge(3, 2, weight=1)

        assert has_parallel_edges(dir_topology) == use_multigraph

        fnss.set_capacities_constant(dir_topology, 10)
        fnss.set_delays_constant(dir_topology, 2)
        with pytest.raises(ValueError):
            fnss.set_buffer_sizes_bw_delay_prod(dir_topology)

    def test_buffers_size_link_bandwidth(self):
        fnss.set_buffer_sizes_link_bandwidth(self.topo)
        assert all(data_dict['buffer'] is not None
                   for data_dict in self.topo.edges.values())

    def test_buffers_size_link_bandwidth_default_size(self, topology_converter, use_multigraph):
        topo = topology_converter(fnss.line_topology(4))
        # duplicate every edge, strip edge key to add new edge (materialize before adding)
        topo.add_edges_from([link[:2] for link in topo.edges.keys()])

        assert has_parallel_edges(topo) == use_multigraph

        assert topo.number_of_edges() == 6 if use_multigraph \
            else 3

        fnss.set_capacities_constant(topo, 8, 'Mbps', [(0, 1)])
        fnss.set_capacities_constant(topo, 16, 'Mbps', [(1, 2)])
        fnss.set_buffer_sizes_link_bandwidth(topo, buffer_unit='bytes', default_size=10)
        assert topo.graph['buffer_unit'] == 'bytes'
        for link in extend_link_tuple_to_all_parallel(topo, 0, 1):
            assert topo.edges[link]['buffer'] == 1000000
        for link in extend_link_tuple_to_all_parallel(topo, 1, 2):
            assert topo.edges[link]['buffer'] == 2000000
        for link in extend_link_tuple_to_all_parallel(topo, 2, 3):
            assert topo.edges[link]['buffer'] == 10
        fnss.clear_buffer_sizes(topo)
        for link in extend_link_tuple_to_all_parallel(topo, 2, 3):
            assert 'capacity' not in topo.edges[link]
        with pytest.raises(ValueError):
            fnss.set_buffer_sizes_link_bandwidth(topo)

    def test_buffers_size_constant(self):
        fnss.set_buffer_sizes_constant(self.topo, 65000, buffer_unit='bytes')
        assert all(data_dict['buffer'] == 65000
                   for data_dict in self.topo.edges.values())

    def test_buffers_size_constant_unit_mismatch(self, use_multigraph, topology_converter):
        # If I try to set buffer sizes to some interfaces using a unit and some
        # other interfaces already have buffer sizes assigned using a different
        # unit, then raise an error and ask to use the unit previously used
        topo = topology_converter(fnss.line_topology(3))
        # duplicate every edge, strip edge key to add new edge (materialize before adding)
        topo.add_edges_from([link[:2] for link in topo.edges.keys()])

        assert has_parallel_edges(topo) == use_multigraph

        fnss.set_buffer_sizes_constant(topo, 10, 'packets', [(0, 1)])
        with pytest.raises(ValueError):
            fnss.set_buffer_sizes_constant(topo, 200, 'bytes', [(1, 2)])

    def test_get_buffer_sizes(self):
        fnss.set_buffer_sizes_constant(self.topo, 65000, buffer_unit='bytes')
        buffers = fnss.get_buffer_sizes(self.topo)
        assert sum(buffer_size == 65000 for buffer_size in buffers.values()) == len(self.topo.edges)
